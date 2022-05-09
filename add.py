from app import db,Faculty,Subject,Equation,Component

faculty = Faculty.query.filter_by(name='W9').first()
subject = Subject.query.filter_by(name='Przenoszenie ciepla').first()
equation = Equation.query.filter_by(name='Reynolds').first()



inputed_name = input('Type name: ')
inputed_const = input('Type const: ')

new_thing = Component(name=inputed_name, constant=inputed_const, equation=equation)

db.create_all()
db.session.add(new_thing)
db.session.commit()



print('Added!')