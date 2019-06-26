package dm_sets_extractor;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

public class FolderNameToggler {

    public static void main(String args[]) throws Exception {
        try {
            //incomplete
            String path = "C:\\Users\\user\\Documents\\OCTGN\\GameDatabase\\bb784fc6-fe21-4603-90d7-82c049908a74\\Sets\\";
            //boolean renameToID = true;

            File root = new File(path);
            String imageRootPath = path.replace("GameDatabase", "ImageDatabase");

            System.out.println("Path is " + root.getAbsoluteFile() + "\nImage Path is " + imageRootPath);

            String[] folders = root.list();
            Boolean isNamedAsID = (folders[0].lastIndexOf("-") == folders[0].length() - 13);   //pretty loose check, 
            //should probabably use a prompt whether to rename to set name or set ID
            System.out.println(isNamedAsID ? "Foldes are ID names" : "Folders are set names");

            for (String folder : folders) {
                System.out.println("FolderPath = "+path+folder);
                File setFile = new File(path + folder + "\\set.xml");
                File newFolder = new File(path+getNameFromFile(setFile, isNamedAsID));

                System.out.println(path+folder +" will be renamed to "+newFolder.getCanonicalPath()); // will throw exception if fileName is invalid

                File oldFolder = new File(folder);
                //oldFolder.renameTo(newFolder);
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
                break;
            }
        }
        //System.out.println("Line is "+line);
        String searchParam = "id=";
        if (getName) {
            searchParam = "name=";
        }

        int i = line.indexOf(searchParam);  //check for error here if i < 0 pls

        i = i + 6;
        int j = line.indexOf("\"", i);
        int k = line.indexOf(":", i);
        if (k != -1) {
            j = k;
        }
        
        sc.close();
        return line.substring(i, j);

    }

}
