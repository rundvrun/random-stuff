// InvokeDll.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <windows.h>
#include <stdio.h>

struct ITabFile {
    int (**_vptr_ITabFile)(...);
};
// HMODULE hinstLib, hKernel, hAdvapi, hGDI, hIMM, hLua;
BOOL fFreeResult, fRunTimeLinkSuccess = FALSE;
int proc;

//typedef void(***__cdecl typeweird (char* a1, int a2, int a3))(void);
typedef ITabFile* (__cdecl typeweird)(char*, int, int);
typedef DWORD* (__cdecl typeweird1)(char*, int, int);
typedef bool (__cdecl typee)(struct ITabFile** a1, const char* a2, int a3, int a4);

void (***__cdecl g_OpenTabFile (char* a1, int a2, int a3))(void) {
    return NULL;
}

void* unknown_libname_1 (void* a)
{
    *(DWORD*)a = 0;
    return a;
}

DWORD* sub_406D10 (DWORD* a)
{
    DWORD* result; // eax
    DWORD* v2; // [esp+0h] [ebp-4h]

    v2 = a;
    result = a;
    if (!*a)
        return result;
    result = (DWORD*)(*(int (__thiscall**)(DWORD))(*(DWORD*)*a + 4))(*a);
    *v2 = 0;
    return result;
}

int sub_406BB0 (DWORD* a, int a2)
{
    DWORD* v2; // ST00_4

    v2 = a;
    sub_406D10 (a);
    *v2 = a2;
    return a2;
}

int unknown_libname_170 (void* a)
{
    return *(DWORD*)a;
}

int main()
{
    //HMODULE hKernel = LoadLibrary (L"kernel32.dll");
    //HMODULE hAdvapi = LoadLibrary (L"ADVAPI32.dll");
    //SetCurrentDirectory (L".");
    /*HMODULE hGDI = LoadLibrary (L"GDI32.dll");
    // HMODULE hIMM = LoadLibrary (L"IMME32.dll");
    HMODULE hLua = LoadLibrary (L"LuaLibDll.dll");
    // HMODULE hMSP90 = LoadLibrary (L"MSVCP90.dll");
    // HMODULE hMSR90 = LoadLibrary (L"MSVCR90.dll");
    HMODULE hNet = LoadLibrary (L"NETAPI32.dll");
    HMODULE hOle = LoadLibrary (L"ole32.dll");
    HMODULE hOleA = LoadLibrary (L"OLEAUT32.dll");
    HMODULE hShell = LoadLibrary (L"SHELL32.dll");
    HMODULE hUser = LoadLibrary (L"USER32.dll");
    HMODULE hVer = LoadLibrary (L"VERSION.dll");
    HMODULE hW2S = LoadLibrary (L"WS2_32.dll");*/
    HMODULE hinstLib = LoadLibrary (L"rundvrun11.dll");
    //FreeLibrary(hW2S);
    DWORD dw = GetLastError ();
    typeweird* procc;
    typeweird1* procc1;

    //char v156;


    //void (***t)(void);
    ITabFile* t = new ITabFile;
    if (hinstLib != NULL) {
        proc = (int)GetProcAddress (hinstLib, "g_OpenTabFile");
        if (NULL != proc) {
            fRunTimeLinkSuccess = TRUE;

            procc = (typeweird*)proc;
            procc1 = (typeweird1*)proc;
            t = procc ((char *)"C:\\rundvrun", 0, 0);
            auto v3 = procc1((char*)"C:\\rundvrun", 0, 0);
            auto cc = (*(int(__thiscall**)(DWORD))(*(DWORD*)v3 + 20))((DWORD)v3) - 1;
            int nHeight = 0;
            nHeight = (*((int (__cdecl**)(ITabFile*))t->_vptr_ITabFile + 5))(t);
            //printf ("%d\n", nHeight);
            //int* nGenre = (int*)malloc(sizeof(int));
            //int* nDetail = (int*)malloc (sizeof (int));
            //int* nParticular = (int*)malloc (sizeof (int));
            char c = '\0';
            char szBuffer[32];
            bool ok = false;
            int coln = 0;
            do
            {
                char buffer[512];
                (*((void (__thiscall**)(ITabFile*, int, signed int, void*, char*, signed int))t->_vptr_ITabFile + 7))(
                    t,
                    1,
                    ++coln,
                    &c,
                    buffer,
                    512);
                ok = buffer[0] != '\0';
            } while (ok);

            for (int row = 1; row <= nHeight; ++row) {
                int col = 0;
                do
                {
                    char buffer[512];
                    (*((void (__thiscall**)(ITabFile*, int, signed int, void*, char*, signed int))t->_vptr_ITabFile + 7))(
                        t,
                        row,
                        ++col,
                        &c,
                        buffer,
                        512);
                    ok = buffer[0] != '\0' || col < coln;

                    printf ("%s%c", buffer, ok ? '\t' : '\n');
                } while (ok);
                //printf ("\n");
            }
            /*char longBuff[256];
            //unknown_libname_1 (&v156);
            //int v1 = (int)t;
            //sub_406BB0 ((DWORD*)&v156, v1);
            //int v4 = unknown_libname_170 (&v156);

            (*((int (__thiscall**)(ITabFile*, int, signed int, DWORD, int*))t->_vptr_ITabFile + 10))(
                t,
                i + 1,
                2,
                0,
                nGenre);
            printf ("%d\n", *nGenre);

            (*((int (__thiscall**)(ITabFile*, int, signed int, DWORD, int*))t->_vptr_ITabFile + 10))(
                t,
                i + 1,
                3,
                0,
                nDetail);
            printf ("%d\n", *nDetail);

            (*((int (__thiscall**)(ITabFile*, int, signed int, DWORD, int*))t->_vptr_ITabFile + 10))(
                t,
                i + 1,
                4,
                0,
                nParticular);
            printf ("%d\n", *nParticular);

            (*((void (__thiscall**)(ITabFile*, int, signed int, void*, char*, signed int))t->_vptr_ITabFile + 7))(
                    t,
                    i + 1,
                    1,
                    &c,
                    szBuffer,
                    32);
            printf ("%s\n", szBuffer);

            (*((void (__thiscall**)(ITabFile*, int, signed int, void*, char*, signed int))t->_vptr_ITabFile + 7))(
                t,
                i + 1,
                2,
                &c,
                longBuff,
                256);
            printf ("%s\n", longBuff);*/
            /*(*(int (__thiscall**)(int, int, signed int, DWORD, __int16*))(*(DWORD*)v4 + 40))(
                v4,
                i + 1,
                3,
                0,
                nDetail);
            printf ("%d\n", *nDetail);

            (*(int (__thiscall**)(int, int, signed int, DWORD, __int16*))(*(DWORD*)v4 + 40))(
                v4,
                i + 1,
                4,
                0,
                nParticular);
            printf ("%d\n", *nParticular);*/
            //delete(t);
            // printf ("%X\n", *t->ptr);

        }
        fFreeResult = FreeLibrary (hinstLib);
        /*fFreeResult = FreeLibrary (hKernel);
        fFreeResult = FreeLibrary (hAdvapi);
        fFreeResult = FreeLibrary (hGDI);
        // fFreeResult = FreeLibrary (hIMM);
        fFreeResult = FreeLibrary (hLua);
        // fFreeResult = FreeLibrary (hMSP90);
        // fFreeResult = FreeLibrary (hMSR90);
        fFreeResult = FreeLibrary (hOle);
        fFreeResult = FreeLibrary (hOleA);
        fFreeResult = FreeLibrary (hShell);
        fFreeResult = FreeLibrary (hUser);
        fFreeResult = FreeLibrary (hVer);
        fFreeResult = FreeLibrary (hW2S);*/
    }
    //printf (fRunTimeLinkSuccess == TRUE ? "Success" : "Fail" "\n");

    return 0;
}

