// pch.cpp: source file corresponding to the pre-compiled header

#include "pch.h"

// When you are using pre-compiled headers, this source file is necessary for compilation to succeed.

DLLExport InitDumper()
{
    std::filesystem::remove_all("logs");
    std::filesystem::remove_all("settings");
    std::filesystem::remove_all("script");
    std::filesystem::remove_all("ui");
    std::filesystem::remove_all("uimage");
    std::filesystem::remove_all("font");
    std::filesystem::remove_all("spr");
    std::filesystem::remove_all("minidump");
    return NULL;
}

DLLExport UnInitDumper()
{
    std::filesystem::remove_all("logs");
    std::filesystem::remove_all("settings");
    std::filesystem::remove_all("script");
    std::filesystem::remove_all("ui");
    std::filesystem::remove_all("uimage");
    std::filesystem::remove_all("font");
    std::filesystem::remove_all("spr");
    std::filesystem::remove_all("minidump");
    return NULL;
}
