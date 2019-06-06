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
 * @author Pranjal/nitrox This is for getting wikia TCG images and then renaming them
 * to the card IDs
 */
public class ImageRenamer {

    int count = 0;

    public static void main(String args[]) throws Exception {
        ImageRenamer temp = new ImageRenamer();
        String set = "DM-18_lul";
        String xmlLocation = "F:\\Duel\\ImageExtraction\\DM-18 Separated Cards\\Separated Cards\\Set18 Best Challenger";
        temp.doIt(set, xmlLocation, false);

    }

    void doIt(String setName, String setFile, boolean makeSetV2) throws Exception {
        BufferedReader in = null;
        PrintWriter filewr = null;
        String dir = "F:\\Duel\\ImageExtraction\\DM-18 Separated Cards\\Separated Cards\\Set18 Best Challenger";
        //String setFile = JOptionPane.showInputDialog("Enter set.xml file address for " + setName);
        setFile += "\\set.xml";
        
        if (makeSetV2) {
            filewr = new PrintWriter(dir + "setBasedOnImage.xml", "UTF-8");
        }
        
        try {
            in = new BufferedReader(new FileReader(setFile));
        } catch (FileNotFoundException e) {
            System.out.println("File " + setFile + " not found!");
        }
        String xmlContents = "";
        String xmlLine;
        while ((xmlLine = in.readLine()) != null) { //MAIN LOOP
            xmlContents += xmlLine;
            int i = xmlLine.indexOf("card name=");
            if (i > 0) {
                {
                    String cardName = xmlLine.substring(i + 11, xmlLine.indexOf("\"", i + 12)).trim();
                    int j = xmlLine.indexOf("id=");
                    String cardID = "";
                    if (j > 0) {
                        cardID = xmlLine.substring(j + 4, xmlLine.indexOf("\"", j + 5)).trim();
                    } else {
                        System.out.println("CARD ID NOT FOUND");
                    }
                    System.out.println(++count + "\tCard is " + cardID + "\t" + cardName);
                    //if(!cardName.equals("Crystal Lancer")) continue;  //wtf
                    System.out.println("Attempting process and rename to ID...");
                    
                    File oldImage = new File(dir + "\\" + cardName + ".jpg");
                    if (oldImage.exists()) {
                        System.out.println("File Found");
                    } else {
                        oldImage = new File(dir + "\\" + cardName.replace(",", "") + ".jpg");
                        if (oldImage.exists()) {
                            System.out.println("File Found");
                        } else {
                            oldImage = new File(dir + "\\" + oldImage.getName().replace("-", " "));
                            if (oldImage.exists()) {
                                System.out.println("File Found");
                            } else {
                                System.out.println("ERROR File not found");
                            }
                        }
                    }
                    if (oldImage.exists()){
                        BufferedImage pic = ImageIO.read(oldImage);
                        int width = pic.getWidth();
                        int height = pic.getHeight();
                        double aspect = (double) width / height;

                        ResampleOp resizeOp = new ResampleOp((int) (aspect * 560), 560);
                        resizeOp.setFilter(ResampleFilters.getLanczos3Filter());  //boy this is nice
                        BufferedImage scaledPic = resizeOp.filter(pic, null);
                        ImageIO.write((RenderedImage) scaledPic, "jpg", new File(dir+"\\"+cardID+".jpg"));
                        
                        //write another set file based on available images - use for adding promos only
                        if (makeSetV2) 
                        {
                            filewr.println(xmlLine);
                            while (!xmlLine.equals("")) 
                            {
                                xmlLine = in.readLine();
                                filewr.println(xmlLine);
                            }
                        }
                    }
                }
            }
        }
        String setID = getID(setName.replace('_', ' '), xmlContents);
        System.out.println("SetID is " + setID);
        in.close();
        if(makeSetV2) filewr.close();
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
        String imgUrl = new ImageExtractor().extractImageUrl(image); //converted
        //System.out.println("Real image url is:" + imgUrl);
        BufferedImage pic = ImageIO.read(new URL(imgUrl));

        int width = pic.getWidth();
        int height = pic.getHeight();
        double aspect = (double) width / height;

        ResampleOp resizeOp = new ResampleOp((int) (aspect * 560), 560);
        resizeOp.setFilter(ResampleFilters.getLanczos3Filter());
        BufferedImage scaledPic = resizeOp.filter(pic, null);
        System.out.println(scaledPic.getType());
        if (scaledPic.getType() == 6) {
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
