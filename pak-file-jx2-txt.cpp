// ConsoleApplication1.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>
#include <fstream>
#include <string>
typedef unsigned long ul;
ul _hash (const char* file_name) {
    ul id = 0;
    const char* ptr = file_name;
    int index = 0;
    while (*ptr) {
        ++index;
        auto val = *ptr + (*ptr >= 'A' && *ptr <= 'Z' ? 32 : 0);
        id = (id + index * val) % 0x8000000b * 0xffffffef;
        ptr++;
    }
    return (id ^ 0x12345678);
}

int main()
{
    std::ifstream myfile ("files_settingc.txt");
    std::ofstream ofile ("file_c.pak.txt");
    std::string line;
    int i = 0;
    if (myfile.is_open ())
    {
        ofile << "TotalFile:13893\tPakTime:2020-4-15 1:31:5\tPakTimeSave:5e960169\tCRC:8a07a505\n";
        ofile << "Index\tID\tTime\tFileName\tSize\tInPakSize\tComprFlag\tCRC\n";

        while (getline (myfile, line))
        {
            ofile << std::dec << i++ << "\t" << std::hex << _hash(line.c_str()) << "\t" << "2020-4-15 1:29:24\t" << line;
            ofile << std::dec << '\t' << 49 << '\t' << 49 << '\t' << 0 << "\tbb67eabb\n";
            // if (i > 20)
            //    break;
        }
        myfile.close ();
        ofile.close ();
    }
    // std::cout << std::hex << _hash("\\script\\skill\\´äÑÌÁéÅ®\\ÓêÁØÁå(õõÕÐ).lua");
}

// Run program: Ctrl + F5 or Debug > Start Without Debugging menu
// Debug program: F5 or Debug > Start Debugging menu

// Tips for Getting Started: 
//   1. Use the Solution Explorer window to add/manage files
//   2. Use the Team Explorer window to connect to source control
//   3. Use the Output window to see build output and other messages
//   4. Use the Error List window to view errors
//   5. Go to Project > Add New Item to create new code files, or Project > Add Existing Item to add existing code files to the project
//   6. In the future, to open this project again, go to File > Open > Project and select the .sln file
