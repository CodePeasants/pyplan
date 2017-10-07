# Python standard library
import weakref
from functools import partial
import unittest
import uuid

# Package
from plan.serializable import Serializable
from plan.serializable import reference
from plan.serializable import weak_reference
from plan.serializable import expand_ids
from plan.serializable import has_id
from plan.serializable import get_id
from plan.serializable import is_id
from plan.settings import ID_KEY
from plan.object_registry import ObjectRegistry


class TestSerializable(unittest.TestCase):

    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        ObjectRegistry.clear()

    def test_id_lazy(self):
        """ID value should remain None until requested or assigned."""
        inst = Basic('foo')
        self.assertIs(None, inst._Serializable__id)
        self.assertTrue(inst.id)

    def test_id_single_assignment(self):
        """ID can only be set once."""
        inst = Basic('foo')
        obj_id = get_id()
        inst.id = obj_id
        self.assertEqual(obj_id, inst.id)
        self.assertRaises(RuntimeError, partial(setattr, inst, 'id', get_id()))

    def test_id_register(self):
        """When an ID is acquired, it is registered with the ObjectRegistry."""
        self.assertFalse(ObjectRegistry.OBJECTS)
        inst = Basic('foo')
        self.assertFalse(ObjectRegistry.OBJECTS)
        inst.id
        self.assertIn(inst.id, list(ObjectRegistry.OBJECTS.keys()))

    def test_to_dict_id(self):
        """Encoding to a dictionary should always write a valid UUID."""
        inst = Basic('bar')
        data = inst.to_dict()
        self.assertIn(ID_KEY, data)
        self.assertEqual(inst.id, data[ID_KEY])

    def test_to_dict_keys(self):
        """Encoding to a dict should always include keys for every argument in the __init__ signature of the object."""
        # Construct a serializable object
        bar = 'bar'
        inst = Basic(bar)
        self.assertEqual(bar, inst.foo)

        data = inst.to_dict()
        self.assertEqual({ID_KEY: inst.id, 'foo': bar}, data)

    def test_to_dict_omit(self):
        """Encoding to a dict should omit any attributes that are not in the __init__ signature."""
        # Construct a serializable object
        inst = Basic('bar')
        inst.bizz = 5
        self.assertEqual(5, inst.bizz)

        data = inst.to_dict()
        self.assertNotIn('bizz', list(data.keys()))

    def test_from_dict(self):
        """Verify that decoding from a dict works as expected."""
        bar = 'bar'
        data = {ID_KEY: get_id(), 'foo': bar}

        inst = Basic.from_dict(data)
        self.assertEqual(bar, inst.foo)
        self.assertEqual(data[ID_KEY], inst._Serializable__id)

    def test_round_trip_basic(self):
        """Verify that encoding to and from a dict properly preserves data."""
        bar = 'bar'
        inst = Basic(bar)
        orig_id = inst.id
        data = inst.to_dict()

        # In this test, we will assume a new interpreter session, so the original object should not be in memory.
        del inst
        self.assertFalse(ObjectRegistry.OBJECTS)

        inst = Basic.from_dict(data)
        self.assertEqual(bar, inst.foo)
        self.assertEqual(orig_id, inst.id)
        self.assertIn(inst.id, list(ObjectRegistry.OBJECTS.keys()))

    def test_round_trip_mutate_replace(self):
        """
        When you decode an object from dict while an object with the same ID is still in memory, the newly decoded
        data should overwrite what was in memory, but use the same object. This will ensure pointers to that object
        do not become stale.
        """
        bar = 'bar'
        bizz = 'bizz'
        inst = Basic(bar)
        inst2 = Basic(inst)  # Create an object that references the original instance.
        orig_id = inst.id
        data = inst.to_dict()

        data['foo'] = bizz

        new_inst = Basic.from_dict(data)
        self.assertIs(new_inst, inst)
        self.assertEqual(bizz, new_inst.foo)
        self.assertEqual(orig_id, new_inst.id)
        self.assertIn(new_inst.id, list(ObjectRegistry.OBJECTS.keys()))
        self.assertIs(new_inst, ObjectRegistry.get(new_inst.id))
        self.assertEqual(bizz, inst2.foo.foo)

    def test_is_id(self):
        """Return True if valid ID."""
        self.assertTrue(is_id(str(uuid.uuid4())))

    def test_is_id_invalid(self):
        """Return False if not valid ID."""
        self.assertFalse(is_id(5))
        self.assertFalse(is_id(6.5))
        self.assertFalse(is_id('bob'))

    def test_expand_ids_basic(self):
        """Expand a UUID into its corresponding Serializable object."""
        inst = Basic('foo')
        obj_id = inst.id
        self.assertIs(inst, expand_ids(obj_id))

    def test_expand_ids_list(self):
        """Expand a UUID nested in a list into its corresponding Serializable object."""
        inst = Basic('foo')
        obj_id = inst.id
        data = [1, 2, obj_id]
        self.assertEqual([1, 2, inst], expand_ids(data))

    def test_expand_ids_tuple(self):
        """Expand a UUID nested in a tuple into its corresponding Serializable object."""
        inst = Basic('foo')
        obj_id = inst.id
        data = (1, 2, obj_id)
        self.assertEqual((1, 2, inst), expand_ids(data))

    def test_expand_ids_dict(self):
        """Expand a UUID nested in a dictionary into its corresponding Serializable object."""
        inst = Basic('foo')
        inst2 = Basic('bar')
        obj_id = inst.id
        obj_id2 = inst2.id
        data = {'bizz': [1, obj_id], 'bazz': obj_id2, 'buzz': {'bizz': (2, obj_id2)}}
        self.assertEqual(
            {'bizz': [1, inst], 'bazz': inst2, 'buzz': {'bizz': (2, inst2)}},
            expand_ids(data)
        )

    def test_has_id_basic(self):
        """Return True if passed a valid ID."""
        self.assertTrue(has_id(get_id()))

    def test_has_id_basic_invalid(self):
        """Return False if passed a basic data type that is not an valid ID."""
        self.assertFalse(has_id(5))
        self.assertFalse(has_id('foobar'))

    def test_has_id_list(self):
        """Return True if a provided list has a contained ID."""
        self.assertTrue(has_id([1, 2, 3, get_id()]))

    def test_has_id_tuple(self):
        """Return True if a provided tuple has a contained ID."""
        self.assertTrue(has_id((1, 2, 3, get_id())))

    def test_has_id_dict(self):
        """Return True if a provided dict has a contained ID."""
        self.assertTrue(has_id({'bizz': get_id()}))

    def test_has_id_nested(self):
        """Return True if a provided nested structure has a contained ID."""
        self.assertTrue(has_id({'bizz': 1, 'bazz': [2, 3], 'buzz': {'bizz': [1, (1, get_id())]}}))

    def test_has_id_nested_invalid(self):
        """Return False if a nested structure does not have an ID."""
        self.assertFalse(has_id({'bizz': 1, 'bazz': [2, 3], 'buzz': {'bizz': [1, (1,)]}}))

    def test_reference(self):
        """Setting and getting a reference normally."""
        pass

    def test_reference_id(self):
        """Set reference property to an ID & getting an object back."""
        pass

    def test_reference_strong(self):
        """Returned object from an ID should be a strong reference."""
        pass

    def test_weak_reference(self):
        """Setting and getting a weak reference normally."""
        pass

    def test_weak_reference_id(self):
        """Set reference property to an ID & getting a weak reference back."""
        pass

    def test_weak_reference_weak(self):
        """Returned object from an ID should be a weak reference."""
        pass

    def test_weak_reference_mismatch(self):
        """
        The weak_reference decorator does not automatically force pointers stored from your property setter to be weak.
        It just ensures that you do not expand an ID to a strong reference, when a weak reference is desired. So in this
        case, we verify that if we explicitly store a strong reference in a property decorated with weak_reference,
        we will actually store a strong reference when the object is created, but get a weak reference when it is
        decoded. This case should be avoided!
        """
        pass

    def test_references_round_trip(self):
        """Integration test where we store weak & strong nested references, encode then decode."""
        pass


class Basic(Serializable):
    """Serializable is an abstract class, we need a concrete implementation to test."""
    def __init__(self, foo):
        super().__init__()
        self.foo = foo


class Reference(Serializable):
    """Serializable is an abstract class, we need a concrete implementation to test."""
    def __init__(self, foo=None, bar=None):
        super().__init__()
        self.__foo = None
        self.__bar = None
        self.__bizz = None
        self.foo = foo
        self.bar = bar

    @reference
    def foo(self):
        return self.__foo

    @foo.setter
    def foo(self, value):
        self.__foo = value

    @weak_reference
    def foo(self):
        return self.__foo

    @foo.setter
    def foo(self, value):
        self.__foo = value


def main():
    unittest.main()


if __name__ == '__main__':
    main()
