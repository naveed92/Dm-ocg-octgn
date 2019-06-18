package dm_sets_extractor;

import java.awt.Image;
import java.awt.image.RenderedImage;
import javax.swing.JOptionPane;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.URL;
import java.util.logging.Level;
import java.util.logging.Logger;
import java.util.UUID;
import javax.imageio.ImageIO;
import javax.swing.JFileChooser;
// GOTTA FIX FOR PSYCHICS -  MANA COST IS NOW "PSYCHIC COST"(wait in wikia or data?)
//For extracting images make folder F:\Duel\ImageExtraction\<setname> to put images into
//please change http to https in the other files

public class SinnanSetExtractor {

    /**
     * Asks for a set url to extract data of every card in the set
     */
    private String formatToAdd = "OCG";  // the format to add for the set
    private String dataPath = "C:\\Users\\user\\Desktop\\Test";  //default path. This folder MUST exist when testing individual card image extaction.
    // During set extration the program will ask you for that path and make a folder.
    // private String imagePath = "C:\\Users\\user\\Desktop\\Test\\images";

    void extractSet(String setName, boolean extractImages) throws Exception {

        if (setName == "") //no setName specified
        {
            setName = JOptionPane.showInputDialog("Enter set name, exactly as it appears in the wikia page url for the set: (Eg. DMR-03_Episode_1:_Gaial_Victory)");
        }

        String setLink = "https://duelmasters.wikia.com/api.php?action=query&prop=revisions&rvprop=content&format=php&titles=" + setName;
        //this query gets all the names of the cards in the set by querying the wikia 
        System.out.println(setLink);
/////////////////////make folder to put data and, optionally, images

        JFileChooser chooser = new JFileChooser();
        chooser.setCurrentDirectory(new java.io.File("."));
        chooser.setDialogTitle("Select folder to put extracted data and images in");
        chooser.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY);
        chooser.setAcceptAllFileFilterUsed(false);

        if (chooser.showOpenDialog(null) == JFileChooser.APPROVE_OPTION) {
            dataPath = chooser.getSelectedFile().toString();
            System.out.println("Trying to create folder " + dataPath + "\\" + setName.substring(0, 6));

            if (new File(dataPath + "\\" + setName.substring(0, 6)).mkdirs()) {
                System.out.println("Folder made");
                if (extractImages) {
                    new File(dataPath + "\\" + setName.substring(0, 6) + "\\Images").mkdirs();
                }
            } else {
                System.out.println("Failed to make folder!");
            }

        } else {
            System.out.println("Cancelled!");
            Exception e = new Exception("Operation cancelled by user!");
            throw e;

        }

        String setFileName = setName.substring(0, 6);

        String filename = dataPath + "\\" + setFileName + "\\" + setFileName + "Data.xml";
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

        try {

            URL page = new URL(setLink);
            in = new BufferedReader(new InputStreamReader(page.openStream()));

            //in = new BufferedReader(new FileReader("F:/Duel/api.php"));
            filewr = new PrintWriter(filename, "UTF-8");
            System.out.println("File is " + filename);

            filewr.println(xmlText);
            System.out.println(xmlText);
            String line;
            String rarity = "";

            while ((line = in.readLine()) != null) {

                if (line.contains("==Contents==") || line.contains("== Contents ==")) {
                    System.out.println("Contents FOUND");
                    break;
                }
            }
            //one line will be skipped, though no probs
            while (!((line = in.readLine()) == null || line.contains("==Cycles==") || line.contains("==Gallery==") || line.contains("[[Category:") || line.contains("==Contents sorted by Civilizations=="))) {
                if (line.contains("[[") && line.contains("]]")) {
                    specialFlag = 0;    //to check the special case where psychic's 2nd side is NOT in the same line
                    int i1 = line.indexOf("[[") + 2, i2 = line.indexOf("]]");
                    String link = line.substring(i1, i2);
                    link = link.replace(" ", "_");
                    System.out.println("\n" + ++count + "Name is " + link);
                    try {
                        details = extract(link, setFileName, extractImages);
                        details += makeXmlLine("Rarity", rarity);

                        //get collector number in set and rarity RIGHT HERE nugga...somehow
                        //rarity DONE, down below in the last else
                        i1 = line.indexOf('*');
                        i2 = line.indexOf('/');
                        if (i1 != -1 && i2 != -1) {
                            details += makeXmlLine("Number", line.substring(i1 + 1, i2));
                        }
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
                            details = extract(link, setFileName, extractImages);
                            details += makeXmlLine("Rarity", rarity);

                            if (specialFlag == 0) {
                                i1 = line.indexOf("<br>") + 5;
                            } else {
                                i1 = line.indexOf('*') + 1;
                            }
                            i2 = line.indexOf('/', i1);
                            if (i1 != -1 && i2 != -1) {
                                details += makeXmlLine("Number", line.substring(i1, i2));
                            } else {
                                System.out.println("ERROR while processing psychic 2nd side");
                                details += "ERROR WHILE PROCESSING PSYCHIC 2nd side";
                            }

                            details += "\t\t</card>";
                            System.out.println(details);
                            filewr.println(details);
                        }
                    } catch (Exception e) {
                        System.out.println("Error, page is probably not a card page. ");
                        e.printStackTrace();
                        count--;
                    }
                } else if (line.contains("'''{{")) {  //rarity, it is taken from the set contents rather than the card page.
                    //doesn't work for some sets for eg DM18
                    int i = line.indexOf("'''{{") + 5;
                    rarity = line.substring(i, line.indexOf("}}", i));
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
        } catch (Exception e) {
            System.out.print("Unknown exception");
        } finally {
            try {
                in.close();
                filewr.close();
                System.out.println("Set data save to file " + filename);

            } catch (IOException ex) {
                ex.printStackTrace();
            }

        }
    }

    String removeBraces(String txt) {
        //System.out.println(txt);
        if (txt.contains("End Step|")) {
            txt = txt.replace("End Step|", "");
        }
        String newTxt = "";
        int end;
        int st;

        for (int i = 0; i < txt.length(); i++) {
            char c = txt.charAt(i);
            if (c == '[' && txt.charAt(i + 1) == '[') { //removing square braces
                i += 2;
                end = txt.indexOf("]]", i);

                String content = txt.substring(i, end);
                if (content.contains("File:") || content.contains("file:")) {
                    i = end + 1;
                    continue;
                }
                st = content.indexOf('|');
                newTxt += content.substring(st + 1);
                i = end + 1;
            } else if (c == '{' && txt.charAt(i + 1) == '{') {  //removing curly braces
                i += 2;
                end = txt.indexOf("}}", i);
                String content = txt.substring(i, end);

                newTxt += expandEffect(content);  // things in {{  }}

                i = end + 1;
            } else {
                newTxt += c;
            }
        }
        return newTxt;
    }

    String expandEffect(String content) {   //for buggy incomplete effects, these things on the wikia query are not fully mentioned as text 
        //System.out.println("Content: " + content);
        int st = content.indexOf('|');
        String effect = "";
        if (st != -1) {
            effect = content.substring(0, st);
            //System.out.println("Effect: " + effect);
            //these next few things are in a weird format in the wikia query result, gotta process.
            switch (effect) {
                case "tooltip":
                    content = content.substring(st + 1, content.length());
                    break;
                case "Blocker":
                    content = "{BLOCKER}";
                    break;
                case "Power Attacker":
                    content = content.replace("|", " +");
                    break;
                case "Space Charge":
                    content = content.replace("|", "-") + ": ";
                    break;
                case "Saver":
                    content = content.replace("|", "- ");
                    break;
                case "Shield Trigger":
                    content = "{SHIELD TRIGGER}";
                    break;
                case "End Step":
                    content = content.replace("End Step|", "");
                    break;
                case "Gachinko Judge 2":
                    content = removeBraces(content.replace("|", " "));
                    content = content.replace("Gachinko Judge 2", "Whenever this creature attacks, you and your opponent play Gachinko Judge. If you win,");
                    break;
                case "Attack Chance":
                    content = content.replace("|", "- ");
                    String atkType = content.substring(content.indexOf("- ") + 2);
                    content += "(Whenever one of your " + atkType + "s attack, you may cast this for no cost.)";
                    break;
                case "Gravity Zero":
                    System.out.println("WARNING: GravityZero encountered! Please check if the effect was donre correctly!");
                    int st2 = content.lastIndexOf('|');
                    String cond = removeBraces(content.substring(st2 + 1));
                    String type = content.substring(st + 1, st2);
                    content = "Gravity Zero-" + cond + ", ";
                    switch (type) {
                        case "creature":
                        case "Creature":
                            content += "you may summon this creature for no cost.";
                            break;
                        case "spell":
                        case "Spell":
                            content += "you may cast this spell for no cost.";
                            break;
                        default:
                            content += "you may play this card for no cost.";
                    }
                    break;
                case "Doron Go":
                    System.out.println("WARNING: Doron GO encountered! Please check if the effect was donre correctly!");
                    content = content.replace("|", "- ");
                    String doronName = content.substring(content.indexOf("- ") + 2);
                    content += "(When this creature is destroyed, you may put an exile creature that has '" + doronName + "' in its name from your hand into the battle zone)";
                    break;

                default:
                    content = effect;
            }

            //   System.out.println("New content: "+content);
            //next is simple expansion for some other effects.
        } else if (content.contains("Gachinko Judge")) {
            content = content.replace("Gachinko Judge", "(Gachinko Judge: Each player reveals the top card of his deck and then puts it on the bottom of his deck. If your revealed card costs the same as or greater than your opponent's revealed card, you win.)");
        } else if (content.contains("Eternal Omega")) {
            content += "(When this creature would leave the battle zone, return it to your hand instead.)";
        } else if (content.trim().equalsIgnoreCase("Blocker")) {
            content = "{BLOCKER}";
        }
        return content;
    }

    String getAttr(String attr, String all) {
        String output, line;
        int i = all.indexOf("| " + attr);
        if (i != -1) {
            line = all.substring(i, all.indexOf("\n", i));

            output = line.substring(line.indexOf("=") + 2);
        } else {
            output = "";
        }
        return output;

    }

    String makeXmlLine(String property, String value) {
        return "\t\t\t<property name=\"" + property + "\" value=\"" + value + "\" />\n";
    }

    /**
     * Extract a card data and image file name
     *
     * @param cardName Name-URL of the card on wikia, for eg.
     * Bolmeteus_Steel_Dragon
     * @return
     */
    String extract(String cardName, String setName, boolean extractImage) throws Exception {
        //NEED TO ENCODE URL
        String url = "https://duelmasters.wikia.com/api.php?action=query&prop=revisions&rvprop=content&format=php&titles=";
        //url += java.net.URLEncoder.encode(cardName, "UTF-8");

        for (int i = 0; i < cardName.length(); i++) {
            char ch = cardName.charAt(i);
            if (ch > 256) {  //check if it's not ASCII, needs to be URL encoded in that case
                url += java.net.URLEncoder.encode("" + ch, "UTF-8");
            } else {
                url += ch;
            }
        }

        URL page = new URL(url);
        System.out.println("URL Check GO\n" + page.toString());

        BufferedReader in = new BufferedReader(new InputStreamReader(page.openStream()));
        String line, details = "\t\t<card ", alltxt = "";
        int i;

        while ((line = in.readLine()) != null) {
            alltxt += line + "\n";          //put all the card details in alltxt
        }
        i = alltxt.indexOf("image = "); //careful!!! Might not be there on page if page is bad/erronous
        if (i == -1) {
            System.out.println("ERROR! Bad card page!");
            throw new Exception("Bad card page!!!");

        }
        cardName = cardName.replace("\"", "\'");
        //all double quotes in teh card name will be changed to single quotes
        //for example Lionel,_Zenith_of_"Ore" ---> Lionel,_Zenith_of_'Ore'
        //because double quotes cause problems with json later.
        UUID id = UUID.randomUUID();

////////////////////////// Image Processing and saving ////////////////////////
        if (extractImage) {
            System.out.println("Image processing started...");
            String card = alltxt.substring(i + 8, alltxt.indexOf("\n", i));        //get the wikia image filename!!
            try {
                String image = "http://duelmasters.wikia.com/wiki/File:" + card;
                //the wikia address of the image, not the actual one. Gotta convert it to the actual url.
                String imgUrl = new ImageExtractor().extractImageUrl(image); //converted
                System.out.println("Real image url is:" + imgUrl);
                Image pic = ImageIO.read(new URL(imgUrl));
                System.out.println("Saving image in " + dataPath + "\\" + setName + "\\images\\");
                ImageIO.write((RenderedImage) pic, "jpg", new File(dataPath + "\\" + setName + "\\images\\" + id + ".jpg"));
            } catch (Exception e) {
                System.out.println("ERROR! during image extraction for the card! You may need to get the image manually!");
            }
        }
////////////////////////////////// Details processing ////////////////////////////
        System.out.println("Details processing started...");

        details += "name=\"" + cardName.replace("_", " ") + "\" id=\"" + id + "\">\n"; //add name  and id
        details += makeXmlLine("Format", formatToAdd);      //add format 
        //details += makeJsonLine("civilization", alltxt);          //add civ - old version - adds just 1 civ 
        i = alltxt.indexOf("civilization = ");
        String temp;
        if (i == -1) {
            System.out.println("Civilization not found!! Assuming card is colorless. Someting might be wron with the card page, please do a manual check.");
            temp = "Zero";
        } else {
            line = alltxt.substring(i, alltxt.indexOf("\n", i));
            temp = line.substring(line.indexOf("=") + 2).trim();

            while (true) {
                i = alltxt.indexOf("| civilization", i + 1);
                if (i == -1) {
                    break;
                }
                line = alltxt.substring(i, alltxt.indexOf("\n", i));
                temp += "/" + line.substring(line.indexOf("=") + 2).trim();             //add all civs
            }
        }

        details += makeXmlLine("Civilization", temp);                            //finish adding civs, already gone to next line          
        details += makeXmlLine("Cost", getAttr("cost", alltxt));   //add cost
        details += makeXmlLine("Type", getAttr("type", alltxt));                //add type

        //code to hande and add races
        temp = "";
        if ((i = alltxt.indexOf("race = ")) != -1) {                   //if race is found
            line = alltxt.substring(i, alltxt.indexOf("\n", i));
            temp += line.substring(line.indexOf("=") + 2);
            //handle all races now down below
            while (true) {
                i = alltxt.indexOf("| race", i + 1);
                if (i == -1) {
                    break;
                }
                line = alltxt.substring(i, alltxt.indexOf("\n", i));
                temp += "/" + line.substring(line.indexOf("=") + 2);             //add all races
            }
            details += makeXmlLine("Race", temp);                                      //finish adding races, already gone to next line          
        } else //no race
        {
            details += makeXmlLine("Race", "");              //race empty
        }

        temp = getAttr("power", alltxt);
        if (temp.equals("")) {
            temp = "0";  //power must be zero
        }
        details += makeXmlLine("Power", temp);

        //now adding effect(rules text)
        i = alltxt.indexOf("effect = ");
        if (i != -1) {
            i = i + 9;
            int i2 = alltxt.indexOf("| ocgeffect");
            if (i2 == -1) {
                i2 = alltxt.indexOf("|ocgeffect");
                if (i2 == -1) {
                    System.out.println("ERROR!!! Can't find end of effect text");
                    details += "ERROR! Can't find end of effect text";
                    return details;
                }
            }
            line = alltxt.substring(i, i2);
            line = removeBraces(line);
            line = line.replace("\n\n", "\\n");
            line = line.replace("\n", "");
            if (line.endsWith("\\n")) {
                line = line + "\b\b";
            }
            line = line.replace("\\n ", "\\n");
            line = line.replace("\\n", "&#xd;&#xa;");
            line = line.replace("<br>", "&#xd;&#xa;");
            line = line.replace("<br> ", "&#xd;&#xa;");
            line = line.replace("#xa; ", "#xa;");

            details += makeXmlLine("Rules", line.replace('\"', '\'').replace("\u25A0", "").trim());
        } else {                            //vanilla card, there's no effect!
            details += makeXmlLine("Rules", "");
        }
        //no flavor text for now
        /*
         line = makeJsonLine("flavor", alltxt).replace("_flavor", "flavor_text");
         line = removeBraces(line);
         for (i = 0; i < line.length(); i++) {
         char ch = line.charAt(i);
         if (!isJap(ch)) {
         details += ch;
         }
         }
         */
        //details += "\"flavor_text\": \"\",\n";
        //details += makeJsonLine("artist", alltxt);
        return details.replace("''", " ");
    }

    void setDataPath(String setName, boolean extractImages) throws Exception {

        JFileChooser chooser = new JFileChooser();
        chooser.setCurrentDirectory(new java.io.File("."));
        chooser.setDialogTitle("Select folder to put extracted data and images in");
        chooser.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY);
        chooser.setAcceptAllFileFilterUsed(false);

        if (chooser.showOpenDialog(null) == JFileChooser.APPROVE_OPTION) {
            dataPath = chooser.getSelectedFile().toString();
            System.out.println("Trying to create folder " + dataPath + "\\" + setName.substring(0, 6));

            if (new File(dataPath + "\\" + setName.substring(0, 6)).mkdirs()) {
                System.out.println("Folder made");
                if (extractImages) {
                    new File(dataPath + "\\" + setName.substring(0, 6) + "\\Images").mkdirs();
                }
            } else {
                System.out.println("Failed to make folder!");
            }

        } else {
            System.out.println("Cancelled!");
            Exception e = new Exception("Operation cancelled by user!");
            throw e;

        }

    }

    void writeDataToFile(String setName, String data) throws Exception {

        String setFileName = setName + "_";
        String filename = dataPath+"\\"+setFileName.substring(0, 6)+"\\"+setFileName.substring(0, 6)+"_Data.xml";

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
        PrintWriter filewr = new PrintWriter(filename, "UTF-8");
        System.out.println("File is " + filename);

        filewr.println(xmlText+"\n"+data);
        
        filewr.close();
    }
}
