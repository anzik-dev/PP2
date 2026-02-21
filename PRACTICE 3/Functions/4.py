def student_info(name, age=18, *subjects, **extra):
    print("Name:", name)    
    print("Age:", age)     
    
    print("Subjects:")
    for subject in subjects:      
        print("-", subject)
    
    print("Extra info:")
    for key, value in extra.items(): 
        print(key, ":", value)

student_info("Anzik", 17, "Math", "Informatics", city="Almaty", grade="11")