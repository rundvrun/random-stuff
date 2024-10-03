#include <windows.h>
#include <stdio.h>

struct IIniFile
{
	int (**_vptr_IIniFile)(...);
};
typedef unsigned int uint32;
#define _DWORD uint32
typedef IIniFile* (__cdecl funcIni)(const char* FileName, int ForceUnpakFile, int ForWrite);
typedef void (__thiscall** func9)(IIniFile*, char*, const char*, void*, char*, signed int);
typedef void (__thiscall** func17)(IIniFile*, char*, const char*, unsigned int, signed int);
typedef void (__thiscall** func10)(IIniFile*, const char*, char*, _DWORD, int*);
typedef int (__thiscall** func4)(IIniFile*, const char*, char*, char*);
typedef int (__thiscall** func13)(IIniFile*, const char*, char*, int*, int);
typedef void (__thiscall** func14)(IIniFile*, const char*, const char*, RECT*, signed int);
typedef void (__thiscall** func12)(IIniFile*, char*, const char*, int*, int*);
typedef int (__thiscall** func19)(IIniFile*, const char*, const char*, signed int);
typedef void (__thiscall** func2)(IIniFile*);
typedef int (__thiscall** func3)(IIniFile*, char*, char*);
typedef int (__thiscall** func5)(IIniFile*);
typedef void (__thiscall** func7)(IIniFile*, int, signed int, void*, char*, signed int);
typedef void (__thiscall** func1)(IIniFile*);
typedef int (__thiscall** func16)(IIniFile*, const char*, char*, int*, int*);

int unknown_libname_184(void* xthis)
{
	return *(_DWORD*)xthis;
}

int main() {
	HMODULE hinstLib = LoadLibrary(L"engine.dll");
	if (hinstLib) {
		auto g_OpenIniFile = (funcIni*)GetProcAddress(hinstLib, "g_OpenIniFile");
		auto iniFile = g_OpenIniFile((char*)"\\settings\\npcres\\DecorateEffectInfo.ini", 0, 0);

		if (iniFile) {
			auto countFnc = **(func5*)(iniFile->_vptr_IIniFile + 5);
			auto c = countFnc(iniFile);
			printf("Count: %d\n", c);
		}
		else {
			printf("Cannot read file\n");
		}

		FreeLibrary(hinstLib);
	}
	else {
		printf("Failed\n");
	}
	return EXIT_SUCCESS;
}
