import java.io.BufferedWriter;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.RandomAccessFile;
import java.util.ArrayList;

public class DecodeStarDict {
  public static byte[] charToByte(char paramChar) {
    int i = paramChar;
    byte[] arrayOfByte = new byte[2];
    for (int j = arrayOfByte.length - 1; j > -1; j--) {
		Integer a=Integer.valueOf(i & 0xFF);
      arrayOfByte[j] = a.byteValue();
      i >>= 8;
    } 
    return arrayOfByte;
  }
  
  public static int byteToInt(byte[] paramArrayOfbyte) {
    int i = 0;
    for (byte b = 0; b < 3; b++) {
      if (paramArrayOfbyte[b] >= 0) {
        i += paramArrayOfbyte[b];
      } else {
        i = i + 256 + paramArrayOfbyte[b];
      } 
      i *= 256;
    } 
    if (paramArrayOfbyte[3] >= 0) {
      i += paramArrayOfbyte[3];
    } else {
      i = i + 256 + paramArrayOfbyte[3];
    } 
    return i;
  }
  
  public static void main(String[] paramArrayOfString) {
    if (paramArrayOfString.length != 3) {
		System.out.println("Convert tu dien StartDict thanh text source cho MDict");
		System.out.println("Copyright by Huy Thang 2004");
      System.out.println("Huong dan su dung:\n\tjava DecodeStarDict idxfile dictfile outputfile");
      System.exit(0);
    } 
    BufferedWriter bufferedWriter = null;
    RandomAccessFile randomAccessFile1 = null, randomAccessFile2 = null;
    try {
      File file = new File(paramArrayOfString[2]);
      randomAccessFile1 = new RandomAccessFile(paramArrayOfString[0], "r");
      randomAccessFile2 = new RandomAccessFile(paramArrayOfString[1], "r");
      OutputStreamWriter outputStreamWriter = new OutputStreamWriter(new FileOutputStream(file), "UTF-8");
      bufferedWriter = new BufferedWriter(outputStreamWriter);
    } catch (Exception exception) {
      exception.printStackTrace();
    } 
    ArrayList<Integer> arrayList = new ArrayList(50);
    int i = 0;
    String str = "";
    byte b = 0;
    try {
      while ((i = randomAccessFile1.read()) != -1) {
        if (i != b)
          arrayList.add(Integer.valueOf(i)); 
        if (i == b) {
          byte[] arrayOfByte1 = new byte[arrayList.size()];
          for (byte b1 = 0; b1 < arrayList.size(); b1++)
            arrayOfByte1[b1] = (byte)Integer.parseInt(arrayList.get(b1).toString()); 
          str = new String(arrayOfByte1, "UTF-8");
          bufferedWriter.write(str, 0, str.length());
          bufferedWriter.newLine();
          int j = randomAccessFile1.readInt();
          int k = randomAccessFile1.readInt();
          byte[] arrayOfByte2 = new byte[k];
          randomAccessFile2.readFully(arrayOfByte2, 0, k);
          str = new String(arrayOfByte2, "UTF-8");
          bufferedWriter.write(str, 0, str.length());
          bufferedWriter.newLine();
          bufferedWriter.write("</>", 0, 3);
          bufferedWriter.newLine();
          arrayList.clear();
        } 
      } 
    } catch (IOException iOException) {
      iOException.printStackTrace();
    } 
    try {
      randomAccessFile1.close();
      randomAccessFile2.close();
      bufferedWriter.close();
	  System.out.println("Chuyen doi thanh cong");
    } catch (IOException iOException) {
      iOException.printStackTrace();
    } 
  }
}
