from app import db,Faculty,Subject,Equation,Component

faculty = Faculty.query.filter_by(name='W9').first()
subject = Subject.query.filter_by(name='Przenoszenie ciepla').first()



inputed_name = input('Type name: ')
inputed_const = input('Type math: ')

new_thing = Equation(name=inputed_name, mathematics=inputed_const, votes=0, subject=subject)

db.create_all()
db.session.add(new_thing)
db.session.commit()

print('Added!')