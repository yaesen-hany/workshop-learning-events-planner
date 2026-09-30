import json
import re
USERS_DATA="users.json"
EVENT_DATA="events.json"
TRANSPORTTATION_DATA="transportation.json"
LEARNING_PLANE_DATA="learning_plan.json"
def load_data(filename):
    try:
        with open(filename, "r") as f:
            data = json.load(f)
        return data
    except (FileNotFoundError, json.JSONDecodeError):
        return []#to read a data
def save_data(data, filename):
    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        return True
    except Exception as e:
        print(f"Error saving data: {e}")
        return False #to save a data
def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        print("This email is not matching for this patterns")
        return False
    return True#to check email
def validate_phone(phone):
    pattern = r'^01[0125]\d{8}$'
    if not re.match(pattern, phone):
        print("This phone number is not matching for this patterns , The phone should be 11")
        return False
    return True#to check phone
def validate_password(password):
    if len(password)<6 and len(password)>10:
        print("The password should be < 6 ")
        return False
    return True
def validate_age(age):
    if not age.isdigit():
        print("the age should be digit")
        return False
    intr_age=int(age)
    if intr_age<18 :
        print("the age should be <18")
        return False
    return True
def validate_gender(gender):
    if gender not in ["M","F"]:
        print ("please enter M or F")
        return False
    return True
def validate_national_id(national_id,):
    pattern = r'^[0-9]{14}$'
    if not re.match(pattern, national_id):
        print("The national_id should be 14")
        return False
    users_data=load_data(USERS_DATA)
    for user in users_data:
        if user["national_id"]==national_id:
            print("the national_id alreadt exist")
            return False
    return True
class users():
    def __init__(self,id_user,name,email,password,gender,phone,age,national_id,governorate="cairo",role="user"):
        self.__id= id_user
        self.__name=name
        self.__email=email
        self.__password=password
        self.__gender=gender
        self.__phone=phone
        self.__age=age
        self.__national_id=national_id
        self.__governorate=governorate
        self.__role=role
    def __str__(self):
        return  f"[{self.__id}] | {self.__name} | {self.__phone} | {self.__governorate}"#to display user
    def save_user(self):
        return{
            "id": self.__id,
    "name": self.__name,
    "email": self.__email,
    "password": self.__password,
    "gender": self.__gender,
    "phone": self.__phone,
    "age":self.__age,
    "national_id":self.__national_id,
    "governorate": self.__governorate,
    "role": self.__role
            }
    def get_id(self):
        return self.__id
    def get_name(self):
        return self.__name
    def get_age(self):
        return self.__age
    def get_phone(self):
        return self.__phone
    def get_governorate(self):
        return self.__governorate
    def get_email(self):
        return self.__email
    def get_password(self):
        return self.__password
    def set_email(self,new_email):
        if  validate_email(new_email):
           self.__email=new_email
    def set_phone(self,new_phone):
        if validate_phone(new_phone):
            self.__phone=new_phone
    def set_password(self,new_password):
        if validate_password(new_password):
            self.__password=new_password
    def set_age(self,new_age):
        if validate_age:
            self.__age=new_age
class Stack:
    def __init__(self):
        self.navigation_stack=[]
    def is_empty(self):
        return len(self.navigation_stack) == 0
    def push(self,navigation_stack):
        self.navigation_stack.append(navigation_stack)
    def pop(self):
        if self.is_empty():
            return None
        return self.navigation_stack.pop()
    def peek(self):
        if self.is_empty():
            return None
        return self.navigation_stack[-1]
def next_user_id(data=USERS_DATA):
        data = load_data(data)
        id_users=[]
        for users in data:
                if match:= re.search(r"\d+",str(users.get("id",""))):
                   id_users.append(int(match.group()))
        if id_users:
            user_id=max(id_users)+1
            return user_id
        return 1
def register_user():
        new_id=next_user_id()
        name=input("Enter your name: ")
        while True:
         email=input("Enter your email:")
         if validate_email(email):
            break
        while True:
            password=input("Enter a password: ")
            if validate_password(password):
                break
        while True:
            gender=input("Enter your gende M or F: ").upper()
            if validate_gender(gender):
                break
        while True:
            phone=input("Enter your phone: ")
            if validate_phone(phone):
                break
        while True:
            age=((input("Enter your age: ")))
            if validate_age(age):
                break
        while True:
            national_id=input("Enter your national_id:")
            if validate_national_id(national_id):
                break
        governorate=input("Enter your governorate: ")
        new_user=users(new_id,name,email,password,gender,phone,int(age),national_id,governorate=governorate)
        data=load_data(USERS_DATA)
        data.append(new_user.save_user())
        save_data(data,USERS_DATA)
        return new_user.save_user()
def login(user_id,password):
    data=load_data(USERS_DATA)
    for users in data:
        if users["id"]==user_id and users["password"]==password:
            return True
    return False
