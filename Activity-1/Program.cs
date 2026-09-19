using System;

namespace CStyleCommentChecker
{
    class Program
    {
        static void Main(string[] args)
        {
            string[] acceptedTests = { "/*a*/", "/**/", "/***/*", "/*aaa*aaa*/", "/*a/a*/" };
            string[] rejectedTests = { "/**", "/**/a/*aa*/", "aaa/**/aa", "/*/*", "/**a/", "//aaaa" };

            Console.WriteLine("--- ACCEPTED TESTS ---");
            foreach (var test in acceptedTests)
            {
                Console.WriteLine($"\"{test}\": {IsCStyleComment(test)}");
            }

            Console.WriteLine("\n--- REJECTED TESTS ---");
            foreach (var test in rejectedTests)
            {
                Console.WriteLine($"\"{test}\": {IsCStyleComment(test)}");
            }
        }

        static bool IsCStyleComment(string input)
        {
            int currentState = 0;

            foreach (char c in input)
            {
                if (c != 'a' && c != '*' && c != '/')
                {
                    return false;
                }

                switch (currentState)
                {
                    case 0:
                        if (c == '/') currentState = 1;
                        else return false;
                        break;

                    case 1:
                        if (c == '*') currentState = 2;
                        else return false;
                        break;

                    case 2:
                        if (c == '*') currentState = 3;
                        else if (c == 'a' || c == '/') currentState = 2;
                        break;

                    case 3:
                        if (c == '/') currentState = 4;
                        else if (c == '*') currentState = 3;
                        else if (c == 'a') currentState = 2;
                        break;

                    case 4:
                        return false;
                }
            }

            return currentState == 4;
        }
    }
}