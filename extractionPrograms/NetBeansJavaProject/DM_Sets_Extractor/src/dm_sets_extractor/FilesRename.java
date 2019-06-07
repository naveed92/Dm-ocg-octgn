package dm_sets_extractor;
/**
 *
 * @author Win7
 */
import java.io.*;

public class FilesRename {

    public static void main(String args[]) throws IOException {

        String path = "C:\\Users\\Win7\\Documents\\NetBeansProjects\\DM_Sets_Extractor\\dm-ocg-octgn-master\\dm-ocg-octgn\\game\\Sets\\";
        File file = new File(path);
        String tempath = null;    
        String[] names = file.list(); //get list of files in the dir

        try {
            for (String name : names) {
                if (new File(path + "\\" + name).isDirectory()) {
                    tempath = path + "\\" + name + "\\";
                    System.out.println("path is " + tempath);
                }
                File f1=new File(tempath+"seta.xml");
                File f2=new File(tempath+"setb.xml");
                
                boolean b=f1.renameTo(f2);
                if(b){ System.out.println("Rename sucess!");
                       File f=new File(tempath+"set.xml");
                       f.delete();
                       f2.renameTo(new File(tempath+"set.xml"));
                }
            }

        } catch(Exception e){
        }
    }
}
