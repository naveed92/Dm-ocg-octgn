package dm_sets_extractor;

import java.io.*;
import java.net.URLEncoder;
import javax.swing.JFileChooser;

//extract from a txt file containing list of cards(exactly as they appear in wikia URL)
//BE CAREFUL, the rarity attached to all will be "PROMO". Need to change to correct rarity later, esp. Victory Rare for V cards.
public class ExtractFromListV2 {

    public static void main(String args[]) {

        String setName = "DMX-19";
        boolean extractImages = true;
        
        setName = setName.substring(0, 6);
        try {
            SinnanSetExtractor extractor = new SinnanSetExtractor();
            System.out.println("Selecting file...");

            JFileChooser chooser = new JFileChooser();
            chooser.setDialogTitle("Select txt file with the list of cards");

            if (chooser.showOpenDialog(null) == JFileChooser.APPROVE_OPTION) {
                File listFile = chooser.getSelectedFile();
                extractor.setDataPath(setName, true);
                BufferedReader br = new BufferedReader(new FileReader(listFile));
               
                String data = "";
                String cardName = ""; 
                System.out.println("Extracting....");
                
                while ((cardName = br.readLine()) != null) {
                    if (cardName.length() > 0) {
                        // Remove the card number in pack
                        String number = cardName.substring(0, cardName.indexOf(' '));
                        cardName = cardName.substring(cardName.indexOf(' ') + 1);
                        System.out.println(cardName);
                        // Replace spaces with underscores as in the card link
                        cardName = cardName.replace(' ', '_');
                        String cardData = extractor.extract(cardName, setName, extractImages);
                        
                        data += cardData
                                + "\t\t\t<property name=\"Rarity\" value=\"Super Rare\" />\n"
                                + "\t\t\t<property name=\"Number\" value=\"" + number + "\" />\n"
                                + "\t\t</card>\n\n";
                        System.out.println(cardData);
                    }
                }
                System.out.println("Finished! Writing to file...");

                data = data + "\t</cards>\n" + "</set>";
                extractor.writeDataToFile(setName, data);

                br.close();

            } else {
                System.out.println("Cancelled!");
            }

        } catch (Exception e) {
            e.printStackTrace();
        }

    }
}
