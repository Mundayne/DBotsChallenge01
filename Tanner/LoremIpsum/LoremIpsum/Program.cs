using System;
using System.IO;

namespace LoremIpsum
{
    class Program
    {
        static void Main(string[] args)
        {
            var loremIpsum = new LoremIpsum();
            Console.WriteLine(loremIpsum.NewLoremIpsum(10, 5));

            Console.Read();
        }
    }
}
