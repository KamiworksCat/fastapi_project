from app import crud
from app.schema.item import ItemCreate
from app.tests.utils import create_random_user
from app.database import db_session


def test_item_crud():
    user = create_random_user()
    item_in = ItemCreate(owner_id=user.id)
    item = crud.item.create_with_owner(
        db_session=db_session, obj_in=item_in, owner_id=user.id
    )
    assert item.owner_id == user.id

    # Test crud item get
    stored_item = crud.item.get(db_session=db_session, obj_id=item.id)
    assert item.id == stored_item.id
    assert item.identifier == stored_item.identifier
    assert item.owner_id == stored_item.owner_id

    # Test crud removing of item
    item2 = crud.item.remove(db_session=db_session, obj_id=item.id)
    item3 = crud.item.get(db_session=db_session, obj_id=item.id)
    assert item3 is None
    assert item2.id == item.id
    assert item2.owner_id == user.id
