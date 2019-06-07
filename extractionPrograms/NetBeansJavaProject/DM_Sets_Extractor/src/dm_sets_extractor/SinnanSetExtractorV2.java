package dm_sets_extractor;

import java.awt.Image;
import java.awt.image.RenderedImage;
import javax.swing.JOptionPane;
import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.URL;
import java.util.logging.Level;
import java.util.logging.Logger;
import java.util.UUID;
import javax.imageio.ImageIO;

public class SinnanSetExtractorV2 extends SinnanSetExtractor {         //this one takes only the NEW CARDS mentioned in the set, stopping conditions vary though

    /**
     * Asks for a set url to extract data of every card in the set
     */
    @Override
    void extractSet(String setName, boolean extractImages) throws Exception {
        
        if (setName.equals("")) {
            setName = JOptionPane.showInputDialog("Enter EXACT Set URL name: (Eg. DMR-03_Episode_1:_Gaial_Victory)");
        }

        String setLink = "http://duelmasters.wikia.com/api.php?action=query&prop=revisions&rvprop=content&format=php&titles=" + setName;
        //this query gets all the names of the cards in the set by querying the wikia 
        String setFileName = setName.substring(0, 6);
        String filename = setFileName + "_Data.xml";
        // String filename = "TestData.txt";
        String details;
        UUID setId = UUID.randomUUID();
        String xmlText = "<?xml version=\"1.0\" encoding=\"utf-8\" standalone=\"yes\"?>\n"
                + "<set xmlns:noNamespaceSchemaLocation=\"CardSet.xsd\" name=\"" + setName.replace("_", " ")
                + "\" id=\"" + setId + "\" gameId=\"bb784fc6-fe21-4603-90d7-82c049908a74\" gameVersion=\"3.0.0.0\" version=\"2.0.0.0\">\n"
                + "	<packaging>\n"
                + "		<pack name=\"Booster\" id=\"" + UUID.randomUUID() + "\">\n"
                + "			<options>\n"
                + "				<option probability=\"0.083\">\n"
                + "					<pick qty=\"1\" key=\"Rarity\" value=\"Super Rare\" />\n"
                + "					<pick qty=\"5\" key=\"Rarity\" value=\"Common\" />\n"
                + "				</option>\n"
                + "				<option probability=\"0.250\">\n"
                + "					<pick qty=\"1\" key=\"Rarity\" value=\"Very Rare\" />\n"
                + "					<pick qty=\"5\" key=\"Rarity\" value=\"Common\" />\n"
                + "				</option>\n"
                + "				<option probability=\"0.667\">\n"
                + "					<pick qty=\"6\" key=\"Rarity\" value=\"Common\" />\n"
                + "				</option>\n"
                + "			</options>\n"
                + "			<pick qty=\"1\" key=\"Rarity\" value=\"Rare\" />\n"
                + "			<pick qty=\"3\" key=\"Rarity\" value=\"Uncommon\"/>\n"
                + "		</pack>\n"
                + "	</packaging>\n"
                + "	<cards>";
        BufferedReader in = null;
        PrintWriter filewr = null;
        int count = 0, specialFlag;
        SinnanSetExtractorV2 swt = new SinnanSetExtractorV2();

        try {

            URL page = new URL(setLink);
            in = new BufferedReader(new InputStreamReader(page.openStream()));
            filewr = new PrintWriter(filename, "UTF-8");

            filewr.println(xmlText);
            System.out.println(xmlText);
            String line;

            while ((line = in.readLine()) != null) {
                if (line.contains("'''New Cards:'''") || line.contains("==New Cards==")) {
                    System.out.println("Contents FOUND");
                    break;
                }
            }
            //one line will be skipped, though no probs
            while (!((line = in.readLine()) == null || line.contains("==Contents==") || line.contains("==Set Features==") || line.contains("==contents==") || line.contains("[[Category:") || line.contains("==Contents sorted by Civilizations=="))) {
                if (line.contains("[[") && line.contains("]]")) {
                    specialFlag = 0;    //to check the special case where psychic's 2nd side is NOT in the same line
                    int i1 = line.indexOf("[[") + 2, i2 = line.indexOf("]]");
                    String link = line.substring(i1, i2);
                    link = link.replace(" ", "_");
                    System.out.println("\n" + ++count + "Name is " + link);
                    try {
                        details = swt.extract(link, setFileName, extractImages);
                        details += makeXmlLine("Rarity", "Promo"); //promo rarity and no number
                        details += makeXmlLine("Number", "");
                        //get collector number in set and rarity RIGHT HERE nugga...somehow
                        //rarity DONE, down below in the last else
                        ////////THIS IS THE DMD PROBLEM, NUMBER IS NOT IN THE SAME FORMAT                      
                        details = details + "\t\t</card>\n";
                        System.out.println(details);
                        filewr.println(details);

                        if (line.contains("a/")) {
                            if (line.contains("b/")) {
                                System.out.println("lol this is psychic 2nd side");

                            } else {                            //when the 2 sides are not on the same line?!(pretty rare, but still needs handling)
                                line = in.readLine();           //check next line
                                if (line.contains("b/")) {
                                    System.out.println("lol this is psychic 2nd side(special case)");
                                    specialFlag = 1;
                                } else //it's not even on the next line?!
                                {
                                    System.out.println("ERROR EOREOREOROER");
                                }
                            }
                            i1 = line.lastIndexOf("[[") + 2;
                            i2 = line.lastIndexOf("]]");
                            link = line.substring(i1, i2);
                            link = link.replace(" ", "_");
                            System.out.println("\n" + count + "Name is " + link);
                            details = swt.extract(link, setFileName, extractImages);
                            details += makeXmlLine("Rarity", "Promo");
                            details += makeXmlLine("Number", "");
                       
                            details += "\t\t</card>";
                            System.out.println(details);
                            filewr.println(details);
                        }
                    } catch (Exception e) {
                        System.out.println("Error, page is probably not a card page.");
                        count--;
                    }
                } else if (line.contains("'''{{")) {  //rarity, it is taken from the set contents rather than the card page.
                    int i = line.indexOf("'''{{") + 5;
                }
                //System.out.println("line in end is" + line);
            }
            in.close();
            filewr.println("\t</cards>\n</set>");
            filewr.close();

        } catch (IOException e) {
            System.out.print("LOL error ioexception");
        } catch (NullPointerException e) {
            System.out.print("LOL error nullpointer");
        } catch (StringIndexOutOfBoundsException e) {
            System.out.print("LOL error string outta bounds");
        } finally {
            try {
                in.close();
                filewr.close();

            } catch (IOException ex) {
                ex.printStackTrace();
            }

        }
    }

}
