# KYROX Database Relationship Standard

**Status:** Canonical / binding

This file is the single source of truth for foreign-key referential actions across KYROX databases.

## Universal cascade policy

Every database foreign-key relationship in KYROX must use both:

- `ON DELETE CASCADE`
- `ON UPDATE CASCADE`

This applies to existing and future foreign keys in both `kyrox-core` and product databases such as `fair-crm`.

## Implementation requirements

1. New Alembic migrations that create a foreign key must declare `ondelete="CASCADE"` and `onupdate="CASCADE"`.
2. ORM `ForeignKey` declarations must match the database policy so future Alembic/autogenerate work cannot drift the schema back to another referential action.
3. Existing foreign keys that use `NO ACTION`, `RESTRICT`, `SET NULL`, `SET DEFAULT`, or omit a referential action must be migrated to CASCADE/CASCADE.
4. No repository, module, migration, or feature may introduce a different foreign-key action unless the product owner explicitly changes this canonical rule first.
5. Application-level delete/update code must not rely on manually reproducing child-row cascade behavior that belongs to the database relationship.

## Explicit exceptions

The product owner accepts these Fair Stand foreign keys. They use `ON UPDATE CASCADE` and `ON DELETE RESTRICT`. Hard delete must not remove or orphan catalog items. Closing a row is `is_active=false`, not `DELETE`.

- `fair_stand_items.item_type` → `fair_stand_item_type.key`
- `fair_stand_items.unit` → `fair_stand_units.unit_key`

A unit key rename updates referencing `fair_stand_items.unit` values inside the same database statement. Application code must not copy that cascade.

## Verification

After schema migrations, PostgreSQL foreign-key constraints must be checked. Every FK must report cascade for both delete and update actions, except the explicit exceptions above. Those exceptions must report `ON UPDATE CASCADE` and `ON DELETE RESTRICT`.

Any other non-CASCADE FK is a schema-policy failure.
