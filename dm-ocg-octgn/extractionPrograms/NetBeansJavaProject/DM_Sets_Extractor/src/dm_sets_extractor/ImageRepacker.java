package dm_sets_extractor;

import com.mortennobel.imagescaling.ResampleFilters;
import com.mortennobel.imagescaling.ResampleOp;
import java.awt.Image;
import java.awt.image.BufferedImage;
import java.awt.image.RenderedImage;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.URL;
import java.util.UUID;
import javax.imageio.ImageIO;
import javax.swing.JOptionPane;
import javax.swing.JFileChooser;
import javax.swing.filechooser.FileNameExtensionFilter;

/**
 *
 * @author Pranjal This is for getting wikia TCG images and then renaming them
 * to the card IDs
 */
public class ImageRepacker {

    int count = 0;

    public static void main(String args[]) throws Exception {
        ImageRepacker temp = new ImageRepacker();
        temp.doIt("DM-11_Eternal_Wave");

    }

    void doIt(String setName) throws Exception {
        String setLink = "http://duelmasters.wikia.com/api.php?action=query&prop=revisions&rvprop=content&format=php&titles=" + setName;
        BufferedReader in = null;
        
        JFileChooser fc = new JFileChooser();
        fc.setToolTipText("Select set.xml for "+setName);
        int ok = fc.showOpenDialog(null);
        if (ok == JFileChooser.APPROVE_OPTION) {
            File file = fc.getSelectedFile();
        }else{
            
        }
        String setFile = JOptionPane.showInputDialog("Enter set.xml file address for " + setName);
        setFile += "\\set.xml";
        try {
            in = new BufferedReader(new FileReader(setFile));
        } catch (FileNotFoundException e) {
            System.out.println("File " + setFile + " not found!");
        }
        String xmlContents = "";
        String xmlLine;
        while ((xmlLine = in.readLine()) != null) {
            xmlContents += xmlLine;
        }
        String setID = getID(setName.replace('_', ' '), xmlContents);
        System.out.println("SetID is " + setID);
        try {

            URL page = new URL(setLink);
            in = new BufferedReader(new InputStreamReader(page.openStream()));

            String line;
            while ((line = in.readLine()) != null) {
                if (line.contains("==Contents==") || line.contains("== Contents ==")) {
                    System.out.println("Contents FOUND");
                    break;
                }
            }
            while (!((line = in.readLine()) == null || line.contains("==Cycles==") || line.contains("==Gallery==") || line.contains("==Trivia==") || line.contains("[[Category:") || line.contains("==Contents sorted by Civilizations=="))) {
                if (line.contains("[[") && line.contains("]]")) {
                    int i1 = line.indexOf("[[") + 2, i2 = line.indexOf("]]");
                    String link = line.substring(i1, i2);
                    link = link.replace(" ", "_");
                    System.out.println("\n" + ++count + "Name is " + link);
                    try {
                        String cardName = link.replace('_', ' ').replace('Ü', 'U');
                        String cardID = getID(cardName, xmlContents);
                        System.out.println(cardName + "  " + cardID);
                        String details = extractImage(link, cardID, setID);
                    } catch (Exception e) {
                        System.out.println("Error, processing card.");
                        e.printStackTrace();
                        count--;
                    }
                }
            }
        } catch (Exception e) {
            System.out.print("LOL error exception");
            e.printStackTrace();
        } finally {
            try {
                in.close();

            } catch (IOException ex) {
                ex.printStackTrace();
            }

        }
    }

    String extractImage(String cardName, String cardID, String setID) throws Exception {
        //if(count!=23) return "no";
        URL page = new URL("http://duelmasters.wikia.com/api.php?action=query&prop=revisions&rvprop=content&format=php&titles=" + cardName);
        BufferedReader in = new BufferedReader(new InputStreamReader(page.openStream()));
        String line, details = "\t\t<card ", alltxt = "";
        int i;

        while ((line = in.readLine()) != null) {
            alltxt += line + "\n";          //put all the card details in alltxt
        }
        i = alltxt.indexOf("image = ");
        cardName = cardName.replace("\"", "\'");
////////////////////////// Image Processing and saving ////////////////////////
        String card = alltxt.substring(i + 8, alltxt.indexOf("\n", i));        //get the wikia image filename!!
        String image = "http://duelmasters.wikia.com/wiki/File:" + card;
        //the wikia address of the image, not the actual one. Gotta convert it to the actual url.
        String imgUrl = new ImageExtractor().extractImageUrl(image); //converted, don't ask how
        //System.out.println("Real image url is:" + imgUrl);
        BufferedImage pic = ImageIO.read(new URL(imgUrl));

        int width = pic.getWidth();
        int height = pic.getHeight();
        double aspect = (double) width / height;

        ResampleOp resizeOp = new ResampleOp((int) (aspect * 560), 560);
        resizeOp.setFilter(ResampleFilters.getLanczos3Filter());
        BufferedImage scaledPic = resizeOp.filter(pic, null);
        System.out.println(scaledPic.getType());
        if (scaledPic.getType()==6) {
            ImageIO.write((RenderedImage) scaledPic, "png", new File("C:\\Users\\user\\Documents\\OCTGN\\ImageDatabase\\bb784fc6-fe21-4603-90d7-82c049908a74\\Sets\\" + setID + "\\" + cardID + ".png"));
        } else {
            ImageIO.write((RenderedImage) scaledPic, "jpg", new File("C:\\Users\\user\\Documents\\OCTGN\\ImageDatabase\\bb784fc6-fe21-4603-90d7-82c049908a74\\Sets\\" + setID + "\\" + cardID + ".jpg"));
        }

        return "ok";
    }

    String getID(String cardName, String xmlContents) {
        int i = xmlContents.indexOf(cardName);
        String id = "";
        if (i > 0) {
            i = xmlContents.indexOf("id=\"", i) + 4;
            int j = xmlContents.indexOf("\"", i + 5);
            id = xmlContents.substring(i, j);
        } else {
            System.out.println("CARD NOT FOUND IN THE SET FILE WTF");
        }
        if (id.equals("")) {
            System.out.println("ID NOT FOUNDDDD");
        }
        return id;
    }
}
