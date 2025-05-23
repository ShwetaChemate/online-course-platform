# online-course-platform

***Download the project***

You can either download the ZIP file or clone the repository using:
```bash
   git clone https://github.com/ShwetaChemate/online-course-platform.git
   cd onlinecourseplatform
```

***Set up the database***

Run the following commands to create and apply migrations:
```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

***Create a superuser***

To access the admin panel, create a superuser:
```bash
python3 manage.py createsuperuser
```

***Start the development server***
```bash
python3 manage.py runserver 8008
```

***Logging in***

- When you visit the site, you'll see a login page (http://127.0.0.1:8008/).
  
  <img width="384" alt="Screenshot 2025-04-14 at 12 04 30 PM" src="https://github.com/user-attachments/assets/6eb28319-1a7a-46d7-8634-2cf9f7725475" />


- Use the superuser credentials to log in.

- You’ll be taken to the Django admin panel (http://127.0.0.1:8008/admin/), where you can:

  <img width="1183" alt="Screenshot 2025-04-14 at 12 05 35 PM" src="https://github.com/user-attachments/assets/893fbf9a-df9f-4a43-bb13-f24d870abf06" />

- Add normal users or staff users (http://127.0.0.1:8008/admin/auth/user/).

- Create and manage courses (http://127.0.0.1:8008/admin/courses/course/).


***User Permissions***

- **Superuser**: Can view, add, edit, and delete all courses (published or unpublished) (http://127.0.0.1:8008/admin/courses/course/).

  <img width="1176" alt="Screenshot 2025-04-14 at 1 21 13 PM" src="https://github.com/user-attachments/assets/9ff342d2-9795-4c98-aea9-2072f434ffb9" />

- **Staff user**: Can view all courses but cannot add, edit, or delete them (http://127.0.0.1:8008/admin/courses/course/).

  <img width="1179" alt="Screenshot 2025-04-14 at 1 22 09 PM" src="https://github.com/user-attachments/assets/ee528171-23d7-478b-b9ee-e78dae80c137" />

- **Normal user**: Can only view published courses (http://127.0.0.1:8008/non-admin/courses).

<img width="1187" alt="Screenshot 2025-04-14 at 1 23 12 PM" src="https://github.com/user-attachments/assets/b986a47b-86db-4739-acb2-2790bdc8f0db" />

***Logging Out and Switching Users***

After logging out from the admin panel, you can log in again using a normal user or staff user account to test different access levels.

***Proxy Model: PublishedCourse***

- A proxy model named PublishedCourse is used.

- It inherits from the main Course model.

- It filters and exposes only courses where is_published=True (http://127.0.0.1:8008/published-courses/).

- This helps separate the API for published courses without duplicating the model structure.

<img width="1448" alt="Screenshot 2025-04-14 at 1 15 32 PM" src="https://github.com/user-attachments/assets/271478f3-481b-48ed-ba29-9858f024cdef" />



