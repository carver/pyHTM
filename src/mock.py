#
# (c) Dave Kirby 2001 - 2005
#     mock@thedeveloperscoach.com
#
# Original call interceptor and call assertion code by Phil Dawes (pdawes@users.sourceforge.net)
# Call interceptor code enhanced by Bruce Cropley (cropleyb@yahoo.com.au)
#
# This Python  module and associated files are released under the FreeBSD
# license. Essentially, you can do what you like with it except pretend you wrote
# it yourself.
# 
# 
#     Copyright (c) 2005, Dave Kirby
# 
#     All rights reserved.
# 
#     Redistribution and use in source and binary forms, with or without
#     modification, are permitted provided that the following conditions are met:
# 
#         * Redistributions of source code must retain the above copyright
#           notice, this list of conditions and the following disclaimer.
# 
#         * Redistributions in binary form must reproduce the above copyright
#           notice, this list of conditions and the following disclaimer in the
#           documentation and/or other materials provided with the distribution.
# 
#         * Neither the name of this library nor the names of its
#           contributors may be used to endorse or promote products derived from
#           this software without specific prior written permission.
# 
#     THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#     ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#     WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#     DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
#     ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#     (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#     LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
#     ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#     (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#     SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
#         mock@thedeveloperscoach.com


"""
Mock object library for Python. Mock objects can be used when unit testing
to remove a dependency on another production class. They are typically used
when the dependency would either pull in lots of other classes, or
significantly slow down the execution of the test.
They are also used to create exceptional conditions that cannot otherwise
be easily triggered in the class under test.
"""

__version__ = "0.1.0"

# Added in Python 2.1
import inspect
import re

class MockInterfaceError(Exception):
    pass

class Mock:
    """
    The Mock class emulates any other class for testing purposes.
    All method calls are stored for later examination.
    """

    def __init__(self, returnValues=None, realClass=None):
        """
        The Mock class constructor takes a dictionary of method names and
        the values they return.  Methods that are not in the returnValues
        dictionary will return None.
        You may also supply a class whose interface is being mocked.
        All calls will be checked to see if they appear in the original
        interface. Any calls to methods not appearing in the real class
        will raise a MockInterfaceError.  Any calls that would fail due to
        non-matching parameter lists will also raise a MockInterfaceError.
        Both of these help to prevent the Mock class getting out of sync
        with the class it is Mocking.
        """
        self.mockCalledMethods = {}
        self.mockAllCalledMethods = []
        self.mockReturnValues = returnValues or {}
        self.mockExpectations = {}
        self.realClassMethods = None
        if realClass:
            self.realClassMethods = dict(inspect.getmembers(realClass, inspect.isroutine))
            for retMethod in self.mockReturnValues.keys():
                if not self.realClassMethods.has_key(retMethod):
                    raise MockInterfaceError("Return value supplied for method '%s' that was not in the original class" % retMethod)
        self._setupSubclassMethodInterceptors()
     
    def _setupSubclassMethodInterceptors(self):
        methods = inspect.getmembers(self.__class__,inspect.isroutine)
        baseMethods = dict(inspect.getmembers(Mock, inspect.ismethod))
        for m in methods:
            name = m[0]
            # Don't record calls to methods of Mock base class.
            if not name in baseMethods:
                self.__dict__[name] = MockCallable(name, self, handcrafted=True)
 
    def __getattr__(self, name):
        return MockCallable(name, self)
    
    def mockAddReturnValues(self, **methodReturnValues ):
        self.mockReturnValues.update(methodReturnValues)
        
    def mockSetExpectation(self, name, testFn, after=0, until=0):
        self.mockExpectations.setdefault(name, []).append((testFn,after,until))

    def _checkInterfaceCall(self, name, callParams, callKwParams):
        """
        Check that a call to a method of the given name to the original
        class with the given parameters would not fail. If it would fail,
        raise a MockInterfaceError.
        Based on the Python 2.3.3 Reference Manual section 5.3.4: Calls.
        """
        if self.realClassMethods == None:
            return
        if not self.realClassMethods.has_key(name):
            raise MockInterfaceError("Calling mock method '%s' that was not found in the original class" % name)

        func = self.realClassMethods[name]
        try:
            args, varargs, varkw, defaults = inspect.getargspec(func)
        except TypeError:
            # func is not a Python function. It is probably a builtin,
            # such as __repr__ or __coerce__. TODO: Checking?
            # For now assume params are OK.
            return

        # callParams doesn't include self; args does include self.
        numPosCallParams = 1 + len(callParams)

        if numPosCallParams > len(args) and not varargs:
            raise MockInterfaceError("Original %s() takes at most %s arguments (%s given)" % 
                (name, len(args), numPosCallParams))

        # Get the number of positional arguments that appear in the call,
        # also check for duplicate parameters and unknown parameters
        numPosSeen = _getNumPosSeenAndCheck(numPosCallParams, callKwParams, args, varkw)

        lenArgsNoDefaults = len(args) - len(defaults or [])
        if numPosSeen < lenArgsNoDefaults:
            raise MockInterfaceError("Original %s() takes at least %s arguments (%s given)" % (name, lenArgsNoDefaults, numPosSeen))

    def mockGetAllCalls(self):
        """
        Return a list of MockCall objects,
        representing all the methods in the order they were called.
        """
        return self.mockAllCalledMethods
    getAllCalls = mockGetAllCalls  # deprecated - kept for backward compatibility

    def mockGetNamedCalls(self, methodName):
        """
        Return a list of MockCall objects,
        representing all the calls to the named method in the order they were called.
        """
        return self.mockCalledMethods.get(methodName, [])
    getNamedCalls = mockGetNamedCalls  # deprecated - kept for backward compatibility

    def mockCheckCall(self, index, name, *args, **kwargs):
        '''test that the index-th call had the specified name and parameters'''
        call = self.mockAllCalledMethods[index]
        assert name == call.getName(), "%r != %r" % (name, call.getName())
        call.checkArgs(*args, **kwargs)


def _getNumPosSeenAndCheck(numPosCallParams, callKwParams, args, varkw):
    """
    Positional arguments can appear as call parameters either named as
    a named (keyword) parameter, or just as a value to be matched by
    position. Count the positional arguments that are given by either
    keyword or position, and check for duplicate specifications.
    Also check for arguments specified by keyword that do not appear
    in the method's parameter list.
    """
    posSeen = {}
    for arg in args[:numPosCallParams]:
        posSeen[arg] = True
    for kwp in callKwParams:
        if posSeen.has_key(kwp):
            raise MockInterfaceError("%s appears as both a positional and named parameter." % kwp)
        if kwp in args:
            posSeen[kwp] = True
        elif not varkw:
            raise MockInterfaceError("Original method does not have a parameter '%s'" % kwp)
    return len(posSeen)

class MockCall:
    """
    MockCall records the name and parameters of a call to an instance
    of a Mock class. Instances of MockCall are created by the Mock class,
    but can be inspected later as part of the test.
    """
    def __init__(self, name, params, kwparams ):
        self.name = name
        self.params = params
        self.kwparams = kwparams

    def checkArgs(self, *args, **kwargs):
        assert args == self.params, "%r != %r" % (args, self.params)
        assert kwargs == self.kwparams, "%r != %r" % (kwargs, self.kwparams)

    def getParam( self, n ):
        if isinstance(n, int):
            return self.params[n]
        elif isinstance(n, str):
            return self.kwparams[n]
        else:
            raise IndexError, 'illegal index type for getParam'

    def getNumParams(self):
        return len(self.params)

    def getNumKwParams(self):
        return len(self.kwparams)

    def getName(self):
        return self.name
    
    #pretty-print the method call
    def __str__(self):
        s = self.name + "("
        sep = ''
        for p in self.params:
            s = s + sep + repr(p)
            sep = ', '
        items = self.kwparams.items()
        items.sort()
        for k,v in items:
            s = s + sep + k + '=' + repr(v)
            sep = ', '
        s = s + ')'
        return s
    def __repr__(self):
        return self.__str__()

class MockCallable:
    """
    Intercepts the call and records it, then delegates to either the mock's
    dictionary of mock return values that was passed in to the constructor,
    or a handcrafted method of a Mock subclass.
    """
    def __init__(self, name, mock, handcrafted=False):
        self.name = name
        self.mock = mock
        self.handcrafted = handcrafted

    def __call__(self,  *params, **kwparams):
        self.mock._checkInterfaceCall(self.name, params, kwparams)
        thisCall = self.recordCall(params,kwparams)
        self.checkExpectations(thisCall, params, kwparams)
        return self.makeCall(params, kwparams)

    def recordCall(self, params, kwparams):
        """
        Record the MockCall in an ordered list of all calls, and an ordered
        list of calls for that method name.
        """
        thisCall = MockCall(self.name, params, kwparams)
        calls = self.mock.mockCalledMethods.setdefault(self.name, [])
        calls.append(thisCall)
        self.mock.mockAllCalledMethods.append(thisCall)
        return thisCall

    def makeCall(self, params, kwparams):
        if self.handcrafted:
            allPosParams = (self.mock,) + params
            func = _findFunc(self.mock.__class__, self.name)
            if not func:
                raise NotImplementedError
            return func(*allPosParams, **kwparams)
        else:
            returnVal = self.mock.mockReturnValues.get(self.name)
            if isinstance(returnVal, ReturnValuesBase):
                returnVal = returnVal.next()
            return returnVal

    def checkExpectations(self, thisCall, params, kwparams):
        if self.name in self.mock.mockExpectations:
            callsMade = len(self.mock.mockCalledMethods[self.name])
            for (expectation, after, until) in self.mock.mockExpectations[self.name]:
                if callsMade > after and (until==0 or callsMade < until):
                    assert expectation(self.mock, thisCall, len(self.mock.mockAllCalledMethods)-1), 'Expectation failed: '+str(thisCall)


def _findFunc(cl, name):
    """ Depth first search for a method with a given name. """
    if cl.__dict__.has_key(name):
        return cl.__dict__[name]
    for base in cl.__bases__:
        func = _findFunc(base, name)
        if func:
            return func
    return None



class ReturnValuesBase:
    def next(self):
        try:
            return self.iter.next()
        except StopIteration:
            raise AssertionError("No more return values")
    def __iter__(self):
        return self

class ReturnValues(ReturnValuesBase):
    def __init__(self, *values):
        self.iter = iter(values)
        

class ReturnIterator(ReturnValuesBase):
    def __init__(self, iterator):
        self.iter = iter(iterator)

        
def expectParams(*params, **keywords):
    '''check that the callObj is called with specified params and keywords
    '''
    def fn(mockObj, callObj, idx):
        return callObj.params == params and callObj.kwparams == keywords
    return fn


def expectAfter(*methods):
    '''check that the function is only called after all the functions in 'methods'
    '''
    def fn(mockObj, callObj, idx):
        calledMethods = [method.getName() for method in mockObj.mockGetAllCalls()]
        #skip last entry, since that is the current call
        calledMethods = calledMethods[:-1]
        for method in methods:  
            if method not in calledMethods:
                return False
        return True
    return fn

def expectException(exception, *args, **kwargs):
    ''' raise an exception when the method is called
    '''
    def fn(mockObj, callObj, idx):
        raise exception(*args, **kwargs)
    return fn


def expectParam(paramIdx, cond):
    '''check that the callObj is called with parameter specified by paramIdx (a position index or keyword)
    fulfills the condition specified by cond.
    cond is a function that takes a single argument, the value to test.
    '''
    def fn(mockObj, callObj, idx):
        param = callObj.getParam(paramIdx)
        return cond(param)
    return fn

def EQ(value):
    def testFn(param):
        return param == value
    return testFn

def NE(value):
    def testFn(param):
        return param != value
    return testFn

def GT(value):
    def testFn(param):
        return param > value
    return testFn

def LT(value):
    def testFn(param):
        return param < value
    return testFn

def GE(value):
    def testFn(param):
        return param >= value
    return testFn

def LE(value):
    def testFn(param):
        return param <= value
    return testFn

def AND(*condlist):
    def testFn(param):
        for cond in condlist:
            if not cond(param):
                return False
        return True
    return testFn

def OR(*condlist):
    def testFn(param):
        for cond in condlist:
            if cond(param):
                return True
        return False
    return testFn

def NOT(cond):
    def testFn(param):
        return not cond(param)
    return testFn

def MATCHES(regex, *args, **kwargs):
    compiled_regex = re.compile(regex, *args, **kwargs)
    def testFn(param):
        return compiled_regex.match(param) != None
    return testFn

def SEQ(*sequence):
    iterator = iter(sequence)
    def testFn(param):
        try:
            cond = iterator.next()
        except StopIteration:
            raise AssertionError('SEQ exhausted')
        return cond(param)
    return testFn

def IS(instance):
    def testFn(param):
        return param is instance
    return testFn

def ISINSTANCE(class_):
    def testFn(param):
        return isinstance(param, class_) 
    return testFn

def ISSUBCLASS(class_):
    def testFn(param):
        return issubclass(param, class_) 
    return testFn

def CONTAINS(val):
    def testFn(param):
        return val in param 
    return testFn

def IN(container):
    def testFn(param):
        return param in container
    return testFn

def HASATTR(attr):
    def testFn(param):
        return hasattr(param, attr)
    return testFn

def HASMETHOD(method):
    def testFn(param):
        return hasattr(param, method) and callable(getattr(param, method))
    return testFn

CALLABLE = callable



