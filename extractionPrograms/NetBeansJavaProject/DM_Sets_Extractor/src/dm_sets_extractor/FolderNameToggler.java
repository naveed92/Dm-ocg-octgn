package dm_sets_extractor;

import java.io.File;
import java.util.Scanner;

public class FolderNameToggler 
{

    public static void main(String args[]) throws Exception {
        try {
        //incomplete
        String path = "";
        //boolean renameToID = true;
        
        File root = new File(path);
        String imageRootPath = path.replace("GameDatabase","ImageDatabase");
        
        System.out.println("Path is "+root.getAbsoluteFile()+"\nImage Path is "+imageRootPath); 
        
        
        String[] folders = root.list();
        Boolean isNamedAsID = (folders[0].lastIndexOf("-") == folders[0].length()-13);   //pretty loose check, 
        //should probabably use a prompt whether to rename to set name or set ID
        
        for(String folderPath : folders)
        {
            File setFile = new File(folderPath+"/set.xml");            
            File newFolder = new File(getNameFromFile(setFile, isNamedAsID));
            
            System.out.println(f.getCanonicalPath()); // will throw exception if fileName is invalid
            
            File oldFolder = new File(folderPath);
            oldFolder.renameTo(newFolder);
        }
        
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
    
    public static String getSetNameFromFile(File setFile, boolean getName){
        //put shit to get set name or id here
        Scanner sc = new Scanner(setFile);
        
        while(sc.hasNextLine())
        {
            String line=sc.nextLine();
            int i = line.indexOf("Cardset.xsd");
            if(i>0) break;
        }
        
        if(getName){
            int i = line.indexOf("name=");  //check for error here if i < 0 pls
            
            i= i+ 6;
            int j = line.indexOf("\"",i);
                return line.
        }
    }

}
