<h3 align="center">Course-Catalog</h3>

<p align="center">
  Online learning platform built with Python and Django.
</p>

## 📝 Table of Contents

- [About](#about)
- [Installation](#installation)
- [Tech Stacks](#tech)

## 🧐 About <a name = "about"></a>

An online learning hub where individuals can sign up as either mentors or students. Mentor memberships must be verified by the admin before mentors can upload video courses on various subjects, sharing their expertise with the community. Students can watch the courses, rate the content, and leave comments for further engagement



## Installation <a name="installation"></a>

1. First clone the project.

2. Install ``` virtualenv``` if you dont have it.

```
  $ pip install virtualenv
```

3. Create and acivate the virtual environment
```
  $ python -m virtualenv env
  $ env\Scripts\activate
```

4. Install the requirements
```
  $ pip install -r requirements.txt
```

5. Make database migrations
```
  $ python manage.py makemigrations && python manage.py migrate
```

6. Run the server
```
  $ python manage.py runserver
```

## ⛏️ Tech stack <a name = "tech"></a>
- [Python](https://www.python.org/doc/) v3.10.7
- [PostgresSQL](https://www.postgresql.org/docs/current/index.html) v16.0
- [Django](https://docs.djangoproject.com/en/5.1/) v4.2
- [django-rest-framework](https://www.django-rest-framework.org/) v3.15.2
- [pytest](https://docs.pytest.org/en/stable/)


