# Python standard library
import weakref
from functools import partial
import unittest

# Package
from plan.user import User
from plan.serializable import Serializable
from plan.serializable import reference
from plan.settings import ID_KEY
from plan.object_registry import ObjectRegistry


class TestSerializable(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = User('foo')

    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        ObjectRegistry.clear()

    def test_serializable(self):
        class Foo(Serializable):
            """Serializable is an abstract class, we need a concrete implementation to test."""
            def __init__(self, foo):
                super().__init__()
                self.foo = foo

        # Construct a serializable object
        bar = 'bar'
        inst = Foo(bar)
        self.assertEqual(bar, inst.foo)

        # Verify the state of the object registry.
        self.assertFalse(ObjectRegistry.OBJECTS)

        # Encode the object to a dictionary & verify results.
        data = inst.to_dict()
        self.assertEqual({ID_KEY: inst.id, 'foo': bar}, data)
        self.assertIn(data[ID_KEY], list(ObjectRegistry.OBJECTS.keys()))

        # Can not set ID after it has already been set.
        self.assertRaises(RuntimeError, partial(setattr, inst, 'id', 'foo'))

        # Decode the dictionary and compare with the original object.
        new_inst = Foo.from_dict(data)
        self.assertEqual(inst.foo, new_inst.foo)
        self.assertEqual(bar, new_inst.foo)
        self.assertEqual(data[ID_KEY], new_inst.id)

    def test_reference(self):
        class Foo(Serializable):
            """Serializable is an abstract class, we need a concrete implementation to test."""
            def __init__(self, foo=None):
                super().__init__()
                self.__foo = None
                self.foo = foo

            def __repr__(self):
                return '<{0.__class__.__name__} id={0.id}>'.format(self)

            @reference
            def foo(self):
                return self.__foo

            @foo.setter
            def foo(self, value):
                self.__foo = value

        # Ensure we are starting with a clean regisrty
        self.assertFalse(ObjectRegistry.OBJECTS)

        # Construct a pair of objects that reference one another.
        foo1 = Foo()
        foo2 = Foo(foo1)
        # Keep references acyclic. Note: we could actually use cyclic references here, but if we did, we'd have to
        # manually trigger garbage collection to ensure the ObjectRegistry got cleaned up.
        foo1.foo = weakref.proxy(foo2)

        # Serialize the objects.
        data1 = foo1.to_dict()
        data2 = foo2.to_dict()

        # Clear memory to test deserialization.
        del foo1, foo2
        self.assertFalse(ObjectRegistry.OBJECTS)

        foo1 = Foo.from_dict(data1)
        # Since foo2 has not yet been deserialized, trying to pre-emptively request it should fail.
        self.assertRaises(LookupError, partial(getattr, foo1, 'foo'))

        # Deserialize foo2 and verify that both objects and their references have been preserved.
        foo2 = Foo.from_dict(data2)
        self.assertIn(data2[ID_KEY], list(ObjectRegistry.OBJECTS.keys()))
        self.assertEqual(data1[ID_KEY], foo1.id)
        self.assertEqual(data2[ID_KEY], foo2.id)
        self.assertIs(foo2, foo1.foo)
        self.assertIs(foo1, foo2.foo)


def main():
    unittest.main()


if __name__ == '__main__':
    main()
