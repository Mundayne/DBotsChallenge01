using System;
using System.Globalization;
using System.IO;

namespace LoremIpsum
{
    public class LoremIpsum
    {
        //Read all text from the file
        private string[] _Content = File.ReadAllText("Input.txt").Split(' ');

        public string NewLoremIpsum(int sentencesInParagraph, int paragraphs)
        {
            string output = "\t";
            //create paragraph
            for (int i = 0; i < paragraphs; i++)
            {
                //create sentences
                for (int j = 0; j < sentencesInParagraph; j++)
                {
                    //create sentence
                    string[] sentence = new string[new Random().Next(5, 15)];

                    for (int k = 0; k < sentence.Length; k++)
                    {
                        //get a random word from the content
                        int random = new Random().Next(0, _Content.Length);
                        //if it's the beginning of the sentence, capitalize it
                        if (k == 0)
                            sentence[k] = CultureInfo.CurrentCulture.TextInfo.ToTitleCase(_Content[random]);
                        //if it's the ending of the sentence, add a period
                        else if (k == (sentence.Length - 1))
                            sentence[k] = _Content[random] + ". ";
                        //else, just add the word
                        else
                            sentence[k] = _Content[random];
                    }

                    output += string.Join(' ', sentence);
                }
                output += "\n\t";
            }
            output = output.Replace("\r", string.Empty);
            return output;
        }
    }
}
