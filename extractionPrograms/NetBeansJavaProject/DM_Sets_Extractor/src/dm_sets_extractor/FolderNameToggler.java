package dm_sets_extractor;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

public class FolderNameToggler {

    public static void main(String args[]) throws Exception {
        try {
            //incomplete
            File current = new File(new File(".").getCanonicalPath());
            String path = current.getParentFile().getParentFile().getParentFile().getCanonicalPath();
            path = path + "\\GameDatabase\\bb784fc6-fe21-4603-90d7-82c049908a74\\Sets\\";

            File root = new File(path);
            String imagePath = path.replace("GameDatabase", "ImageDatabase");

            System.out.println("Path is " + root.getAbsoluteFile() + "\nImage Path is " + imagePath);

            String[] folders = root.list();
            boolean renameToNames = false;  //controls what the program renames to - names or IDs

            if (folders[0].length() == 36 && folders[0].charAt(23) == '-') {
                System.out.println("Folder names are IDs, renaming to setNames");
                renameToNames = true;
            } else {
                System.out.println("Folder names are set names, renaming to setIDs");

            }

            for (String folder : folders) {
                System.out.println("FolderPath = " + path + folder);
                File setFile = new File(path + folder + "\\set.xml");
                String newFolderName = getNameFromFile(setFile, renameToNames);
                File newFolder = new File(path + newFolderName);
                File oldFolder = new File(path + folder);

                System.out.println(path + folder + " will be renamed to " + newFolder.getCanonicalPath()); // will throw exception if fileName is invalid

                if (!newFolder.exists()) {
                    oldFolder.renameTo(newFolder);
                } else {
                    System.out.println("wtf Folder already exists!");
                }
                
                System.out.println("Now renaming image folder...");
                oldFolder = new File(imagePath+folder);
                newFolder = new File(imagePath + newFolderName);
                if (!newFolder.exists()) {
                    oldFolder.renameTo(newFolder);
                } else {
                    System.out.println("wtf image Folder already exists!");
                }

                
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static String getNameFromFile(File setFile, boolean getName) throws FileNotFoundException {
        //put shit to get set name or id here
        Scanner sc = new Scanner(setFile);
        String line = "";
        while (sc.hasNextLine()) {
            line = sc.nextLine();
            int i = line.indexOf("et.xsd");
            if (i > 0) {
                break; //found
            }
        }
        //System.out.println("Line is "+line);
        String searchParam = "id=";
        if (getName) {
            searchParam = "name=";
        }

        int i = line.indexOf(searchParam);  //check for error here if i < 0 pls

        i = i + 4;  //when it's id move 4 chars front
        if (getName) {
            i += 2;  //when it's name move 2 more
        }
        int j = line.indexOf("\"", i);
        int k = line.indexOf(":", i);
        if (k != -1) {
            j = k;
        }

        sc.close();
        return line.substring(i, j);

    }

}
