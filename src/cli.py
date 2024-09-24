import click
from sqlalchemy.orm import Session
from src.database import SessionLocal, engine
from src.models import Landlord, Tenant, Property, Base

# Create all tables
Base.metadata.create_all(bind=engine)

@click.group()
def cli():
    """Real Estate Management CLI"""
    pass

@cli.command()
@click.argument('name')
def create_landlord(name):
    """Create a new landlord with the specified NAME."""
    db: Session = SessionLocal()  # Start a new database session
    landlord = Landlord(name=name)  # Create a new Landlord instance
    db.add(landlord)  # Add the new landlord to the session
    db.commit()  # Commit the session
    db.refresh(landlord)  # Refresh the landlord instance
    click.echo(f"Landlord {landlord.name} created!")

@cli.command()
@click.argument('name')
@click.argument('rent_amount', type=float)
@click.argument('landlord_id', type=int)
def create_property(name, rent_amount, landlord_id):
    """Create a new property with the specified NAME, RENT_AMOUNT, and LANDLORD_ID."""
    db: Session = SessionLocal()  # Start a new database session
    property = Property(name=name, rent_amount=rent_amount, landlord_id=landlord_id)  # Create a new Property instance
    db.add(property)  # Add the new property to the session
    db.commit()  # Commit the session
    db.refresh(property)  # Refresh the property instance
    click.echo(f"Property {property.name} created with rent amount {property.rent_amount}!")

@cli.command()
@click.argument('name')
@click.argument('age', type=int)
@click.argument('property_id', type=int)
@click.argument('rent_balance', type=float)
def create_tenant(name, age, property_id, rent_balance):
    """Create a new tenant with the specified NAME, AGE, PROPERTY_ID, and RENT_BALANCE."""
    db: Session = SessionLocal()  # Start a new database session
    tenant = Tenant(name=name, age=age, property_id=property_id, rent_balance=rent_balance)  # Create a new Tenant instance
    db.add(tenant)  # Add the new tenant to the session
    db.commit()  # Commit the session
    db.refresh(tenant)  # Refresh the tenant instance
    click.echo(f"Tenant {tenant.name} created for property {tenant.property.name} with a balance of {tenant.rent_balance}!")

@cli.command()
@click.argument('landlord_id', type=int)
@click.argument('new_name')
def edit_landlord(landlord_id, new_name):
    """Edit an existing landlord's name."""
    db: Session = SessionLocal()  # Start a new database session
    landlord = db.query(Landlord).filter(Landlord.id == landlord_id).first()  # Find the landlord by ID
    if landlord:
        landlord.name = new_name  # Update the landlord's name
        db.commit()  # Commit the session
        click.echo(f"Landlord ID {landlord_id} updated to {new_name}.")
    else:
        click.echo(f"Landlord ID {landlord_id} not found.")

@cli.command()
@click.argument('property_id', type=int)
@click.argument('new_name')
@click.argument('new_rent_amount', type=float)
def edit_property(property_id, new_name, new_rent_amount):
    """Edit an existing property's details."""
    db: Session = SessionLocal()  # Start a new database session
    property = db.query(Property).filter(Property.id == property_id).first()  # Find the property by ID
    if property:
        property.name = new_name  # Update the property name
        property.rent_amount = new_rent_amount  # Update the rent amount
        db.commit()  # Commit the session
        click.echo(f"Property ID {property_id} updated to {new_name} with rent amount {new_rent_amount}.")
    else:
        click.echo(f"Property ID {property_id} not found.")

@cli.command()
@click.argument('tenant_id', type=int)
@click.argument('new_name')
@click.argument('new_age', type=int)
@click.argument('new_rent_balance', type=float)
def edit_tenant(tenant_id, new_name, new_age, new_rent_balance):
    """Edit an existing tenant's details."""
    db: Session = SessionLocal()  # Start a new database session
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()  # Find the tenant by ID
    if tenant:
        tenant.name = new_name  # Update the tenant's name
        tenant.age = new_age  # Update the tenant's age
        tenant.rent_balance = new_rent_balance  # Update the rent balance
        db.commit()  # Commit the session
        click.echo(f"Tenant ID {tenant_id} updated to {new_name}, age {new_age}, rent balance {new_rent_balance}.")
    else:
        click.echo(f"Tenant ID {tenant_id} not found.")

@cli.command()
@click.argument('landlord_id', type=int)
def delete_landlord(landlord_id):
    """Delete a landlord by ID."""
    db: Session = SessionLocal()  # Start a new database session
    landlord = db.query(Landlord).filter(Landlord.id == landlord_id).first()  # Find the landlord by ID
    if landlord:
        db.delete(landlord)  # Delete the landlord from the session
        db.commit()  # Commit the session
        click.echo(f"Landlord ID {landlord_id} deleted.")
    else:
        click.echo(f"Landlord ID {landlord_id} not found.")

@cli.command()
@click.argument('property_id', type=int)
def delete_property(property_id):
    """Delete a property by ID."""
    db: Session = SessionLocal()  # Start a new database session
    property = db.query(Property).filter(Property.id == property_id).first()  # Find the property by ID
    if property:
        db.delete(property)  # Delete the property from the session
        db.commit()  # Commit the session
        click.echo(f"Property ID {property_id} deleted.")
    else:
        click.echo(f"Property ID {property_id} not found.")

@cli.command()
@click.argument('tenant_id', type=int)
def delete_tenant(tenant_id):
    """Delete a tenant by ID."""
    db: Session = SessionLocal()  # Start a new database session
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()  # Find the tenant by ID
    if tenant:
        db.delete(tenant)  # Delete the tenant from the session
        db.commit()  # Commit the session
        click.echo(f"Tenant ID {tenant_id} deleted.")
    else:
        click.echo(f"Tenant ID {tenant_id} not found.")

@cli.command()
def list_landlords():
    """List all landlords."""
    db: Session = SessionLocal()  # Start a new database session
    landlords = db.query(Landlord).all()  # Query all landlords from the database
    for landlord in landlords:
        click.echo(f"Landlord: {landlord.name} (ID: {landlord.id})")

@cli.command()
def list_properties():
    """List all properties."""
    db: Session = SessionLocal()  # Start a new database session
    properties = db.query(Property).all()  # Query all properties from the database
    for property in properties:
        click.echo(f"Property: {property.name}, Rent: {property.rent_amount}, Landlord: {property.landlord.name} (ID: {property.id})")

@cli.command()
def list_tenants():
    """List all tenants."""
    db: Session = SessionLocal()  # Start a new database session
    tenants = db.query(Tenant).all()  # Query all tenants from the database
    for tenant in tenants:
        click.echo(f"Tenant: {tenant.name}, Age: {tenant.age}, Property: {tenant.property.name}, Rent Balance: {tenant.rent_balance} (ID: {tenant.id})")

if __name__ == "__main__":
    cli()  # Run the CLI application
