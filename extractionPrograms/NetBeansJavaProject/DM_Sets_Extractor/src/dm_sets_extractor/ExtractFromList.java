package dm_sets_extractor;

import java.io.*;
import javax.swing.JFileChooser;

public class ExtractFromList {

    public static void main(String args[]) {

        String setName = "E3_Promos";
        boolean extractImages = false;
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
                String cardName = br.readLine();

                System.out.println("Extracting....");
                while (cardName != null) {
                    System.out.println(cardName);
                    String cardData = extractor.extract(cardName, setName, extractImages);

                    data += cardData
                            + "\t\t<property name=\"Rarity\" value=\"Promotional\" />\n"
                            + "\t\t<property name=\"Number\" value=\"None\" />"
                            + "\t\t</card>\n";
                    System.out.println(cardData);

                    cardName = br.readLine(); //next card or null if file end reached
                }
                System.out.println("Finished! Wring to file...");

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
