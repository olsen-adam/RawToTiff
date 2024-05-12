import os, sys, time, rawpy, imageio, tqdm

def printIntro(animation=True):
    
    clearScreen()
    
    title = """
 _____       __          __  _          _______ _____ ______ ______ 
|  __ \     /\ \        / / | |        |__   __|_   _|  ____|  ____|
| |__) |   /  \ \  /\  / /  | |_ ___      | |    | | | |__  | |__   
|  _  /   / /\ \ \/  \/ /   | __/ _ \     | |    | | |  __| |  __|  
| | \ \  / ____ \  /\  /    | || (_) |    | |   _| |_| |    | |     
|_|  \_\/_/    \_\/  \/      \__\___/     |_|  |_____|_|    |_|     
    """
    
    footer = "By Adam Olsen"
    length = len(title.splitlines()[1])

    if animation:
        for line in title.splitlines():
            print(line)
            sys.stdout.flush()
            time.sleep(0.1)

        print(" " * (length - len(footer)), end="")
        for letter in footer:
            print(letter, end="")
            sys.stdout.flush()
            time.sleep(0.05)
        
        time.sleep(3)
    else:
        print(title)
        print(" " * (length - len(footer)) + footer)

def clearScreen():
    os.system("cls" if os.name == "nt" else "clear")

def printMenu():
    printIntro(animation=False)
    menu = """
    1. Convert one image in "Old Photos" folder
    2. Convert all images in "Old Photos" folder
    3. Exit
    """
    print(menu)
   
def getImageName():
    if os.listdir("Old Photos") == []:
        print("No images found in the 'Old Photos' folder. Exiting...")
        exit(0)
    while True:
        imageName = input("Enter the name of the image file (e.g. 'DSC00256.raw'): ")
        if os.path.exists(f"Old Photos/{imageName}"):
            break
        else:
            print("Image not found. Please try again. (Make sure the image is in the 'Old Photos' folder)")
    return [imageName]

def getAllImageNames():
    imageList = []
    for file in os.listdir("Old Photos"):
        if file.lower().endswith(".arw"):
            imageList.append(file)
        else:
            print(f"Skipping {file} because it is not an ARW file.")
    return sorted(imageList)

def convertImages(imageList):
    oldFolderPath = "Old Photos/"
    newFolderPath = "New Photos/"
    
    clearScreen()
    print("Converting images...")
    
    completedImages = 0
    
    for n in tqdm.tqdm(range(len(imageList)),bar_format='{l_bar}{bar:20}{r_bar}{bar:-10b}'):
        with rawpy.imread(oldFolderPath + imageList[n]) as raw:
            rgb = raw.postprocess()
        imageio.imsave(newFolderPath + imageList[n].replace(".ARW", ".TIFF"), rgb)
        completedImages += 1
        
    return completedImages

def exitMessage(nImagesCompleted, nImagesTotal):
    print(f"Successfully converted {nImagesCompleted}/{nImagesTotal} images.")
    print("Exiting...")
    time.sleep(2)
    exit(0)

def main():
    printIntro()
    choice = None
    while not choice:
        printMenu()
        choice = input("Enter your choice: ")
        if choice == "1":
            imageList = getImageName()
        elif choice == "2":
            imageList = getAllImageNames()
        elif choice == "3":
            print("Goodbye!")
            exit(0)
        else:
            print("Invalid choice. Please try again.")
            choice = None
            time.sleep(2)
    
    if not imageList:
        print("No images found. Exiting...")
        exit(0)
    
    userInput = input(f"Confirming conversion of {len(imageList)} images. Continue? (y/n): ").lower()
    if userInput == "y":
        nImagesCompleted = convertImages(imageList)
        exitMessage(nImagesCompleted, len(imageList))
    else:
        main()   
     
if __name__ == "__main__":
    main()