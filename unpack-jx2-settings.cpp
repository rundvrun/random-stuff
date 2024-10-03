
#include <windows.h>
#include <stdio.h>

typedef int (__cdecl str_to_int)(const char*);

struct ITabFile {
    int (**_vptr_ITabFile)(...);
};
typedef ITabFile* (__cdecl typeweird)(char*, int, int);

int main()
{
    HMODULE hinstLib = LoadLibrary(L"rundvrun-.dll");
    if (hinstLib) {
        auto proc = (int)GetProcAddress(hinstLib, "g_OpenTabFile");
        auto procc = (typeweird*)proc;
        auto t = procc((char*)"C:\\rundvrun", 0, 0);
        auto nHeight = (*((int(__cdecl**)(ITabFile*))t->_vptr_ITabFile + 5))(t);

        char c = '\0';
        bool ok = false;
        int coln = 0;
        do
        {
            char buffer[2048];
            (*((void(__thiscall**)(ITabFile*, int, signed int, void*, char*, signed int))t->_vptr_ITabFile + 7))(
                t,
                1,
                ++coln,
                &c,
                buffer,
                2048);
            ok = buffer[0] != '\0';
        } while (ok);

        for (int row = 1; row <= nHeight; ++row) {
            int col = 0;
            do
            {
                char buffer[2048];
                (*((void(__thiscall**)(ITabFile*, int, signed int, void*, char*, signed int))t->_vptr_ITabFile + 7))(
                    t,
                    row,
                    ++col,
                    &c,
                    buffer,
                    2048);
                ok = buffer[0] != '\0' || col < coln;

                printf("%s%c", buffer, ok ? '\t' : '\n');
            } while (ok);
        }

        FreeLibrary(hinstLib);
    }
    return EXIT_SUCCESS;
}


int mainold()
{
    HMODULE hinstLib = LoadLibrary (L"engine1.dll");
    int proc = NULL;
    str_to_int* g_FileNameHash;
    DWORD dw = GetLastError ();
    if (hinstLib != NULL) {
        proc = (int)GetProcAddress (hinstLib, "g_FileNameHash");
        if (NULL != proc) {
            g_FileNameHash = (str_to_int*)proc;
            int t = g_FileNameHash ("\\settings\\npc\\boss_setting\\ÌìÒõ½ÌÈ¼Ñ×É±ÊÖ.ini");
            printf ("%X", t);
        }
        FreeLibrary (hinstLib);
    }
    return EXIT_SUCCESS;
}
