# Write-Ups for the FCSC 2021



## Write-Up - Suspicious SMS




### Challenge discovery

 

We are given a file, **jc_dump.bin**, that is a dump of a Java card applet.

We also have an APDU that is a response of the applet.

The aim is to decrypt this APDU.



### Information gathering



Javacard is a framework maintained by Oracle to create applets for small cards (sim cards, ...). I quickly learned that it is possible to convert Javacard applications to java classes, as it is composed of a subset of the Java bytecode.



I spent a lot of hard times trying to find cool tools that could convert Javacard applications to java classes. I even borrowed the Oracle account of a friend to download all the Javacard SDK in the Oracle site!



However, the perfect tool was more obvious to find than I thought. I found the following forum post https://stackoverflow.com/questions/50083585/convert-java-applet-cap-file-to-class-for-decompilation in which a user talks about a tool name **normalizer**, which is part of the Javacard SDK.



By searching it on Google, it appears the tool (and all the SDK) is publicly available on a github:

 https://github.com/martinpaljak/oracle_javacard_sdks/tree/master/jc305u3_kit



I tried it but failed to decompile the jc_dump.bin file.

```
.\normalizer.bat normalize -i .\jc_dump.cap -p ..\api_export_files\ -o test

Normalizer [v3.0.5]
    Copyright (c) 1998, 2015, Oracle and/or its affiliates. All rights reserved.



[ INFO: ] Cap File to Class File conversion in process.
Lors de la lecture du fichier CAP
```



I searched then for a cap file that I could use as an example and tired some of the examples present in this list https://github.com/EnigmaBridge/javacard-curated-list.

This one was already compiled and could be decompiled by the normalizer https://github.com/vletoux/GidsApplet/releases/download/1.3/GidsApplet.cap.



```
.\normalizer.bat normalize -i .\GidsApplet.cap -p ..\api_export_files\ -o test

Normalizer [v3.0.5]
    Copyright (c) 1998, 2015, Oracle and/or its affiliates. All rights reserved.



[ INFO: ] Cap File to Class File conversion in process.
java/lang/Object
javacard/framework/Applet
javacard/framework/OwnerPIN
java/lang/Object
java/lang/Exception
java/lang/Exception
java/lang/Exception
java/lang/Object
java/lang/Object
java/lang/Object
java.lang.RuntimeException: java.lang.ClassNotFoundException: com.mysmartlogon.gidsApplet.CAA
[ INFO: ] Converter [v3.0.5]
[ INFO: ]     Copyright (c) 1998, 2015, Oracle and/or its affiliates. All rights reserved.


error: IO error when parsing OAA.class
converter internal error.
java.lang.NullPointerException
        at com.sun.javacard.classfile.JPackage.resolve(JPackage.java:73)
        at com.sun.javacard.converter.Converter.convert(Converter.java:165)
        at com.sun.javacard.converter.ConverterHarness.generateJCA(ConverterHarness.java:225)
        at com.sun.javacard.converter.ConverterHarness.convert(ConverterHarness.java:83)
        at com.sun.javacard.converter.ConverterHarness.startConversion(ConverterHarness.java:53)
        at com.sun.javacard.components.caputils.CapProcessor.processCap(CapProcessor.java:139)
        at com.sun.javacard.components.ClassicCAPFile.<init>(ClassicCAPFile.java:35)
        at com.sun.javacard.normalizer.NormalizeCommand.execute(NormalizeCommand.java:103)
        at com.sun.javacard.cli.Tool.executeTool(Tool.java:207)
        at com.sun.javacard.cli.Tool.runTool(Tool.java:138)
        at com.sun.javacard.normalizer.Main.execute(Main.java:32)
        at com.sun.javacard.normalizer.Main.main(Main.java:63)
```



Despite the stack trace, it seems the normalizer managed to recover the classes of the example file.

```
ls .\test\com\mysmartlogon\gidsApplet\


    Répertoire : D:\Téléchargements\oracle_javacard_sdks\jc305u1_kit\bin\test\com\mysmartlogon\gidsApplet


Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----        03/05/2021     21:31             83 AAA.class
-a----        03/05/2021     21:31           2033 BAA.class
-a----        03/05/2021     21:31           2664 CAA.class
-a----        03/05/2021     21:31           6487 DAA.class
-a----        03/05/2021     21:31           2191 EAA.class
-a----        03/05/2021     21:31            398 FAA.class
-a----        03/05/2021     21:31            398 GAA.class
-a----        03/05/2021     21:31           1109 HAA.class
-a----        03/05/2021     21:31            290 IAA.class
-a----        03/05/2021     21:31            398 JAA.class
-a----        03/05/2021     21:31           2344 KAA.class
-a----        03/05/2021     21:31            461 LAA.class
-a----        03/05/2021     21:31           4739 MAA.class
-a----        03/05/2021     21:31           9258 NAA.class
-a----        03/05/2021     21:31              0 OAA.class
-a----        03/05/2021     21:31           4289 PAA.class
-a----        03/05/2021     21:31           1041 QAA.class
```





Analyzing the **GidsApplet.cap** file, I found out that it was a Jar archive with the following files:

```
ls .\GidsApplet\com\mysmartlogon\gidsApplet\javacard\


    Répertoire: D:\Téléchargements\oracle_javacard_sdks\jc305u1_kit\bin\GidsApplet\com\mysmartlogon\gidsApplet\javacard


Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
------        17/09/2019     16:02             18 Applet.cap
------        17/09/2019     16:02            349 Class.cap
------        17/09/2019     16:02           1037 ConstantPool.cap
------        17/09/2019     16:02           3008 Descriptor.cap
------        17/09/2019     16:02             34 Directory.cap
------        17/09/2019     16:02             22 Header.cap
------        17/09/2019     16:02             44 Import.cap
------        17/09/2019     16:02          12116 Method.cap
------        17/09/2019     16:02           1335 RefLocation.cap
------        17/09/2019     16:02             13 StaticField.cap
```



This is definitely not the file I have. 



### Decompiling the CAP dump



After some xxd  manipulation on the cap files of the example and the jc_dump.bin file, I found some particularities:

- Each cap file starts with a byte of value between 1 and 11, then 2 bytes that correspond to its size.
- The jc_dump.bin file seems to be a concatenation of the cap files of the jar, with the same headers present inside it.



I decided then to search for the Javacard specification. I found it here : https://www.oracle.com/java/technologies/java-card/platform-specification-v222.html. After downloading it, many PDF are available. I found the interesting information in the JCVM PDF. The CAP file format is described from page 63. 



I learned that the format of a CAP file is indeed

```
component {
	u1 tag
	u2 size
	u1 info[]
}
```

with u1 = 1 byte and u2 = 2 bytes



I also learned that  the different components are ordered as follows:

| Component Type              | Value | File name        |
| --------------------------- | ----- | ---------------- |
| COMPONENT_Header            | 1     | Header.cap       |
| COMPONENT_Directory         | 2     | Directory.cap    |
| COMPONENT_Applet            | 3     | Applet.cap       |
| COMPONENT_Import            | 4     | Import.cap       |
| COMPONENT_ConstantPool      | 5     | ConstantPool.cap |
| COMPONENT_Class             | 6     | Class.cap        |
| COMPONENT_Method            | 7     | Method.cap       |
| COMPONENT_StaticField       | 8     | StaticField.cap  |
| COMPONENT_ReferenceLocation | 9     | RefLocation.cap  |
| COMPONENT_Export            | 10    | Export.cap       |
| COMPONENT_Descriptor        | 11    | Descriptor.cap   |
| COMPONENT_Debug             | 12    | Debug.cap        |



With all these information, I am now able to split the jc_dump.in file into the right files, to recover the original jar archive. The script I wrote is the following:



```python
with open("jc_dump.bin", "rb") as f:
    data = f.read()

parts = {}

for i in range(10):
    p = data[0]
    l = int.from_bytes(data[1:3], "big")
    parts[p] = data[:3+l]
    data = data[3+l:]
    print(l == len(parts[p]))

labels = ["","Header", "Directory", "Applet", "Import", "ConstantPool", "Class", "Method", "StaticField", "RefLocation", "Export", "Descriptor", "Debug"]

for ind in parts:
    with open(labels[ind]+".cap","wb") as f:
        f.write(parts[ind])
```



Now that I have the right files, I simply replaced those present in the jar archive of the **GidsApplet.cap** applet.



Then I ran the normalizer on it:

```
.\normalizer.bat normalize -i .\GidsApplet3.cap -p ..\api_export_files\ -o dump

Normalizer [v3.0.5]
    Copyright (c) 1998, 2015, Oracle and/or its affiliates. All rights reserved.



[ INFO: ] Cap File to Class File conversion in process.
javacard/framework/Applet
[ INFO: ] Converter [v3.0.5]
[ INFO: ]     Copyright (c) 1998, 2015, Oracle and/or its affiliates. All rights reserved.


javacard/framework/Applet
[ INFO: ] conversion completed with 0 errors and 0 warnings.
```



This time it worked well! It gave me a AAA.class file that I decompile with the jd-gui.exe tool. It produced the following code:



```java
package GidsApplet2.com.mysmartlogon.gidsApplet;

import javacard.framework.APDU;
import javacard.framework.Applet;
import javacard.framework.ISOException;
import javacard.framework.Util;
import javacard.security.AESKey;
import javacard.security.CryptoException;
import javacard.security.Key;
import javacard.security.KeyBuilder;
import javacardx.crypto.Cipher;

public class AAA extends Applet {
  private AESKey field_token0_descoff10;
  
  private Cipher field_token1_descoff17;
  
  public void process(APDU paramAPDU) {
    short s1;
    short s2;
    byte[] arrayOfByte2;
    if (selectingApplet())
      return; 
    byte[] arrayOfByte1 = paramAPDU.getBuffer();
    if (arrayOfByte1[0] != Byte.MIN_VALUE)
      ISOException.throwIt((short)28160); 
    if (arrayOfByte1[2] != 0 || arrayOfByte1[3] != 0)
      ISOException.throwIt((short)27270); 
    switch (arrayOfByte1[1]) {
      case 1:
        s1 = (short)(short)(arrayOfByte1[4] & 0xFF);
        for (s2 = (short)paramAPDU.setIncomingAndReceive(); (short)s1 > 0; s2 = (short)paramAPDU.receiveBytes((short)5))
          s1 = (short)(short)((short)s1 - (short)s2); 
        arrayOfByte2 = method_token255_descoff60(arrayOfByte1, (short)5, (short)(arrayOfByte1[4] & 0xFF));
        Util.arrayCopy(arrayOfByte2, (short)0, arrayOfByte1, (short)0, arrayOfByte2.length);
        paramAPDU.setOutgoingAndSend((short)0, arrayOfByte2.length);
        return;
    } 
    ISOException.throwIt((short)27904);
  }
  
  private byte[] method_token255_descoff60(byte[] paramArrayOfbyte, short paramShort1, short paramShort2) {
    byte[] arrayOfByte = new byte[100];
    try {
      this.field_token1_descoff17.doFinal(paramArrayOfbyte, (short)paramShort1, (short)paramShort2, arrayOfByte, (short)0);
    } catch (CryptoException cryptoException) {
      short s = (short)cryptoException.getReason();
      switch ((short)s) {
        case 5:
          ISOException.throwIt((short)26209);
          break;
        case 1:
          ISOException.throwIt((short)26210);
          break;
        case 4:
          ISOException.throwIt((short)26211);
          break;
        case 3:
          ISOException.throwIt((short)26212);
          break;
        case 2:
          ISOException.throwIt((short)26213);
          break;
      } 
    } catch (Exception exception) {
      ISOException.throwIt((short)26214);
    } 
    return arrayOfByte;
  }
  
  public boolean select() {
    return true;
  }
  
  public static void install(byte[] paramArrayOfbyte, short paramShort, byte paramByte) {
    new AAA(paramArrayOfbyte, (short)paramShort, (short)paramByte);
  }
  
  protected AAA(byte[] paramArrayOfbyte, short paramShort, byte paramByte) {
    short s1 = (short)(short)paramShort;
    short s2 = (short)0;
    byte[] arrayOfByte1 = { 
        80, 25, -2, -82, 77, 43, -86, 123, -111, 35, 
        -84, -123, 68, 104, 111, 102 };
    byte[] arrayOfByte2 = { 
        -54, 73, -103, 59, 115, -4, 110, 122, 100, 98, 
        Byte.MAX_VALUE, -27, Byte.MIN_VALUE, -42, -88, 87 };
    this.field_token0_descoff10 = (AESKey)KeyBuilder.buildKey((byte)15, (short)128, false);
    this.field_token0_descoff10.setKey(arrayOfByte1, (short)0);
    this.field_token1_descoff17 = Cipher.getInstance((byte)23, true);
    this.field_token1_descoff17.init((Key)this.field_token0_descoff10, (byte)2, arrayOfByte2, (short)0, arrayOfByte2.length);
    if ((short)paramByte >= 9) {
      s1 = (short)(short)((short)s1 + (short)(1 + paramArrayOfbyte[(short)paramShort]));
      s1 = (short)(short)((short)s1 + (short)(1 + paramArrayOfbyte[(short)s1]));
      s1 = (short)(s1 + 1);
      s2 = (short)1;
    } 
    if ((short)s2 != 0) {
      register(paramArrayOfbyte, (short)((short)paramShort + 1), paramArrayOfbyte[(short)paramShort]);
    } else {
      register();
    } 
  }
}
```



The code is quite simple to understand. It performs an AES encryption with the key `arrayOfByte1 = { 80, 25, -2, -82, 77, 43, -86, 123, -111, 35, -84, -123, 68, 104, 111, 102 }` and the IV `arrayOfByte2 = { -54, 73, -103, 59, 115, -4, 110, 122, 100, 98, Byte.MAX_VALUE, -27, Byte.MIN_VALUE, -42, -88, 87 }`



I could recover the flag with the following script:



```python
from Crypto.Cipher import AES

key = bytes([80, 25, 256-2, 256-82, 77, 43, 256-86, 123, 256-111, 35, 256-84, 256-123, 68, 104, 111, 102 ])
iv = bytes([256-54, 73, 256-103, 59, 115, 256-4, 110, 122, 100, 98, 127, 256-27, 256 - 128, 256 -42, 256-88, 87 ])
ciphertext = bytes.fromhex("C6 5F 56 69 08 F8 A0 4A 4D CE 35 C0 1A 4B B2 AB 29 D4 1C FC EA 3D FF 7E 97 E3 42 F6 4F 60 27 14 9C C7 83 4A 04 F9 D7 C2 DE 8F 35 0E 96 77 09 6F 81 EA D0 CD 09 FB BE 74 58 D7 FE 45 2D 9D A4 43 11 87 63 31 24 EF 65 3D 6E 55 DF 54 34 AC E0 A5 90 00".replace(" ",""))
aes = AES.new(key, AES.MODE_CBC, iv)

print(aes.decrypt(ciphertext[:-2]))
```



**FCSC{3979b97dcc72b09b2172b4ceea40ab9a5d759e6af4683bcad9886eef6eef12ce}** !

