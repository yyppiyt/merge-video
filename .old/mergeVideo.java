import java.awt.Desktop;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.file.DirectoryStream;
import java.nio.file.Files;
import java.nio.file.InvalidPathException;
import java.nio.file.NoSuchFileException;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.LinkedList;
import java.util.Locale;
import java.util.MissingResourceException;
import java.util.Scanner;

public class mergeVideo {
	public static void main(String args[]) {
		Scanner scanner1 = new Scanner(System.in);
		String ans, inputPath = "", outputPath = "C:\\Videos\\", videoExtension = "mkv", imageExtension = "png",
				subtitleString, trackOrderString, attachmentString, mkvToolCommand;
		Path inputDir = null;
		LinkedList<String> filenames = new LinkedList<String>();
		boolean argsFailed = false, moveToTrash = false;
		LinkedList<String[]> subtitleStringList = new LinkedList<String[]>();
		LinkedList<String[]> attachmentStringList = new LinkedList<String[]>();
		int completedNum = 0, warningNum = 0, abortNum = 0;
		// Enter path
		try {
			inputPath = args[0].replace("\"", "").trim();
			inputDir = Paths.get(inputPath);
			if (!Files.exists(inputDir) || inputPath == "") {
				System.out.println("Path invalid, enter again");
				inputPath = "";
				argsFailed = true;
			}
		} catch (ArrayIndexOutOfBoundsException aioobe) {
			argsFailed = true;
		} catch (InvalidPathException ipe) {
			System.out.println("Path invalid, enter again:");
			argsFailed = true;
		}

		if (argsFailed)
			do {
				try {
					System.out.println("Enter folder path:");
					// inputPath = inputPath.replace("\\", "\\\\");
					inputPath = scanner1.nextLine().replace("\"", "").trim();
					inputDir = Paths.get(inputPath);
					if (!Files.exists(inputDir) || inputPath == "") {
						System.out.println("Path invalid, enter again");
						inputPath = "";
						continue;
					}
					break;
				} catch (InvalidPathException ipe) {
					System.out.println("Path invalid, enter again:");
				}
			} while (true);
		// Change video extension
		do {
			System.out.println("Change video extension? (Y/N) (Default: mkv)");
			ans = scanner1.nextLine();
			if (ans.equalsIgnoreCase("Y")) {
				System.out.println("Enter new video extension:");
				while (true) {
					String newExtension = scanner1.nextLine().replaceAll("\\s", "");
					if (newExtension != "") {
						videoExtension = newExtension;
						break;
					}
					System.out.println("Video extension invalid, enter again:");
				}
			}
		} while (!ans.equalsIgnoreCase("Y") && !ans.equalsIgnoreCase("N"));
		// Change image extension
		do {
			System.out.println("Change image extension? (Y/N) (Default: png)");
			ans = scanner1.nextLine();
			if (ans.equalsIgnoreCase("Y")) {
				System.out.println("Enter new image extension:");
				while (true) {
					String newExtension = scanner1.nextLine().replaceAll("\\s", "");
					if (newExtension != "") {
						imageExtension = newExtension;
						break;
					}
					System.out.println("Image extension invalid, enter again:");
				}
			}
		} while (!ans.equalsIgnoreCase("Y") && !ans.equalsIgnoreCase("N"));
		// Output to subfolder
		do {
			System.out.println("Output to subfolder? (Y/N) (Default directory: C:\\Videos\\)");
			ans = scanner1.nextLine();
			if (ans.equalsIgnoreCase("Y")) {
				System.out.println("Enter subfolder name:");
				while (true) {
					String newOutputPath = scanner1.nextLine(); // .replaceAll("\\s", "");
					if (newOutputPath != "") {
						newOutputPath = (newOutputPath + "\\");
						outputPath += newOutputPath;
						break;
					}
					System.out.println("Name invalid, enter again");
				}
			}
		} while (!ans.equalsIgnoreCase("Y") && !ans.equalsIgnoreCase("N"));
		// Move files to Recycle Bin after merge
		do {
			System.out.println("Move files to Recycle Bin after merge? (Y/N) (Default: N)");
			ans = scanner1.nextLine();
			if (ans.equalsIgnoreCase("Y"))
				moveToTrash = true;
		} while (!ans.equalsIgnoreCase("Y") && !ans.equalsIgnoreCase("N"));

		// Read video and image files
		LinkedList<String> videoFiles = new LinkedList<String>();
		LinkedList<String> imageFiles = new LinkedList<String>();
		// Read video
		try (DirectoryStream<Path> fileStream = Files.newDirectoryStream(inputDir, "*." + videoExtension)) {
			for (Path file : fileStream) {
				String temp = file.getFileName().toString(); // .getBytes("UTF-8"),StandardCharsets.UTF_8);
				int pos = temp.lastIndexOf(".");
				temp = temp.substring(0, pos).replace("&", "^&");
				videoFiles.add(temp);
			}
		} catch (NoSuchFileException nsfe) {
			System.out.println("\nFolder path invalid, program ended");
			System.exit(0);
		} catch (IOException ioe) {
			System.out.println("\nIOException occurred when reading video files, program ended");
			System.exit(0);
		}
		// Read image
		try (DirectoryStream<Path> fileStream = Files.newDirectoryStream(inputDir, "*." + imageExtension)) {
			for (Path file : fileStream) {
				String temp = file.getFileName().toString();
				int pos = temp.lastIndexOf(".");
				temp = temp.substring(0, pos).replace("&", "^&");
				imageFiles.add(temp);
			}
		} catch (NoSuchFileException nsfe) {
			System.out.println("\nFolder path invalid, program ended");
			System.exit(0);
		} catch (IOException ioe) {
			System.out.println("\nIOException occurred when reading image files, program ended");
			System.exit(0);
		}
		// Check video and image
		for (String videoFile : videoFiles) {
			if (imageFiles.contains(videoFile))
				filenames.add(videoFile);
		}
		if (filenames.size() > 0)
			System.out.println("\nFound " + filenames.size() + " files to be progress\n");
		else {
			System.out.println("\nFound 0 files to be progress, program ended");
			System.exit(0);
		}
		// Add subtitle
		do {
			System.out.println("Enter \"List\" to list all file");
			System.out.println("Add subtitle(s)? (Subtitle file must be in the same folder) (Y/N)");
			ans = scanner1.nextLine();
			if (ans.equalsIgnoreCase("List")) {
				System.out.println("\nVideo list: ");
				for (int i = 0; i < filenames.size(); i++)
					System.out.println(i + 1 + ": " + filenames.get(i).replace("^&", "&"));
				System.out.println();
			}
			if (ans.equalsIgnoreCase("Y")) {
				int counter;
				do {
					counter = 1;
					System.out.println("\nVideo list: ");
					for (int i = 0; i < filenames.size(); i++)
						System.out.println(i + 1 + ": " + filenames.get(i).replace("^&", "&"));
					System.out.println("Subtitle: Enter number to choose video (Enter \"Exit\" to quit)");
					ans = scanner1.nextLine();
					try {
						int videoNumber = Integer.parseInt(ans);
						if (--videoNumber >= filenames.size() || videoNumber < 0)
							continue;
						System.out.println("\nChosen video:\n" + filenames.get(videoNumber).replace("^&", "&") + "\n");
						if (!subtitleStringList.isEmpty()) {
							for (String[] subtitleArray : subtitleStringList) {
								if (filenames.get(videoNumber) == subtitleArray[0]) {
									counter++;
								}
							}
						}
						String subtitleFile;
						do {
							// Subtitle name
							do {
								System.out.println("Enter subtitle file " + counter
										+ ": (E.G.:subtitle.srt)(Enter \"Exit\" to quit)");
								subtitleFile = scanner1.nextLine().trim().replace("&", "^&");
							} while (subtitleFile == "");
							if (subtitleFile.equalsIgnoreCase("Exit"))
								continue;
							String subtitleFileLanguage = "";
							Locale localeCheck;
							// Subtitle language
							do {
								try {
									System.out.println("Enter language of subtitle file " + counter +
											": (E.G.:\"en\" for English, \"ja\" for Japanese, \"zh\" for Chinese, \"und\" for Undetermined)");
									subtitleFileLanguage = scanner1.nextLine().replaceAll("\\s", "").toLowerCase();
									localeCheck = new Locale(subtitleFileLanguage);
									localeCheck.getISO3Language();
								} catch (MissingResourceException mre) {
									System.out.println("Unknown language code");
									subtitleFileLanguage = "";
								}
							} while (subtitleFileLanguage == "");
							String[] subtitleArray = { filenames.get(videoNumber), subtitleFile, subtitleFileLanguage };
							// Confirmation
							do {
								System.out.println("\nAdding subtitle " + counter
										+ " (" + subtitleFileLanguage + "):\n\"" + subtitleArray[1].replace("^&", "&")
										+ "\"\ninto\n\"" + subtitleArray[0].replace("^&", "&") + "\"\n(Y/N)");
								ans = scanner1.nextLine();
							} while (!ans.equalsIgnoreCase("Y") && !ans.equalsIgnoreCase("N"));
							if (ans.equalsIgnoreCase("Y")) {
								subtitleStringList.add(subtitleArray);
								System.out.println("\nSubtitle " + (counter++) + " added");
							} else
								System.out.println("\nAction canceled");

						} while (!subtitleFile.equalsIgnoreCase("Exit"));
					} catch (NumberFormatException nfe) {
					}
				} while (!ans.equalsIgnoreCase("Exit"));
				break;
			}
		} while (!ans.equalsIgnoreCase("Y") && !ans.equalsIgnoreCase("N"));
		// Add attachment
		do {
			System.out.println("Enter \"List\" to list all file");
			System.out.println("Add attachment(s)? (Attachment file must be in the same folder) (Y/N)");
			ans = scanner1.nextLine();
			if (ans.equalsIgnoreCase("List")) {
				System.out.println("\nVideo list: ");
				for (int i = 0; i < filenames.size(); i++)
					System.out.println(i + 1 + ": " + filenames.get(i).replace("^&", "&"));
				System.out.println();
			}
			if (ans.equalsIgnoreCase("Y")) {
				int counter;
				do {
					counter = 1;
					System.out.println("\nVideo list: ");
					for (int i = 0; i < filenames.size(); i++)
						System.out.println(i + 1 + ": " + filenames.get(i).replace("^&", "&"));
					System.out.println("Attachment: Enter number to choose video (Enter \"Exit\" to quit)");
					ans = scanner1.nextLine();
					try {
						int videoNumber = Integer.parseInt(ans);
						if (--videoNumber >= filenames.size() || videoNumber < 0)
							continue;
						System.out.println("\nChosen video:\n" + filenames.get(videoNumber).replace("^&", "&") + "\n");
						if (!attachmentStringList.isEmpty()) {
							for (String[] subtitleArray : attachmentStringList) {
								if (filenames.get(videoNumber) == subtitleArray[0]) {
									counter++;
								}
							}
						}
						String attachmentFile;
						do {
							// Attachment name
							do {
								System.out.println("Enter attachment file " + counter
										+ ": (E.G.:attachment.txt)(Enter \"Exit\" to quit)");
								attachmentFile = scanner1.nextLine().trim().replace("&", "^&");
							} while (attachmentFile == "");
							if (attachmentFile.equalsIgnoreCase("Exit"))
								continue;
							String[] attachmentArray = { filenames.get(videoNumber), attachmentFile };
							// Confirmation
							do {
								System.out.println("\nAdding attachment " + counter + ":\n\""
										+ attachmentArray[1].replace("^&", "&") + "\"\ninto\n\""
										+ attachmentArray[0].replace("^&", "&") + "\"\n(Y/N)");
								ans = scanner1.nextLine();
							} while (!ans.equalsIgnoreCase("Y") && !ans.equalsIgnoreCase("N"));
							if (ans.equalsIgnoreCase("Y")) {
								attachmentStringList.add(attachmentArray);
								System.out.println("\nAttachment " + (counter++) + " added");
							} else
								System.out.println("\nAction canceled");

						} while (!attachmentFile.equalsIgnoreCase("Exit"));
					} catch (NumberFormatException nfe) {
					}
				} while (!ans.equalsIgnoreCase("Exit"));
				break;
			}

		} while (!ans.equalsIgnoreCase("Y") && !ans.equalsIgnoreCase("N"));

		// System.out.println("\nDebug");
		// System.exit(0);

		// Merge process
		System.out.println("\n---Merge starts---\n");
		do {
			// MKVTool command variables
			String filename = filenames.getFirst();
			subtitleString = "";
			trackOrderString = "0:0,0:1";
			attachmentString = "";
			int subtitleStringCounter = 0, attachmentStringCounter = 0, mkvmergeExitCode = 0;
			LinkedList<String[]> tempSubtitleStringList = new LinkedList<String[]>();
			LinkedList<String[]> tempAttachmentStringList = new LinkedList<String[]>();
			for (String[] subtitleArray : subtitleStringList) {
				if (filename == subtitleArray[0]) {
					subtitleStringCounter++;
					tempSubtitleStringList.add(subtitleArray);
				}
			}
			for (String[] attachmentArray : attachmentStringList) {
				if (filename == attachmentArray[0]) {
					attachmentStringCounter++;
					tempAttachmentStringList.add(attachmentArray);
				}
			}
			// Update subtitleString, trackOrderString and attachmentString
			if (subtitleStringCounter > 1) {
				for (int i = 1; i <= subtitleStringCounter; i++) {
					if (i == 1) {
						subtitleString += "--language 0:" + tempSubtitleStringList.getFirst()[2] + " ^\"^(^\" ^\""
								+ inputPath + "\\" + tempSubtitleStringList.getFirst()[1] + "^\" ^\"^)^\" ";
					} else {
						subtitleString += "--language 0:" + tempSubtitleStringList.getFirst()[2]
								+ " --default-track-flag 0:no" + " ^\"^(^\" ^\""
								+ inputPath + "\\" + tempSubtitleStringList.getFirst()[1] + "^\" ^\"^)^\" ";
					}
					trackOrderString += ("," + i + ":0");
					tempSubtitleStringList.removeFirst();
				}
			} else if (subtitleStringCounter > 0) {
				subtitleString += "--language 0:" + tempSubtitleStringList.getFirst()[2] + " ^\"^(^\" ^\""
						+ inputPath + "\\" + tempSubtitleStringList.getFirst()[1] + "^\" ^\"^)^\" ";
				trackOrderString = "0:0,0:1,1:0";
			}
			if (attachmentStringCounter > 1) {
				for (int i = 1; i <= attachmentStringCounter; i++) {
					attachmentString += "--attach-file ^\"" + inputPath + "\\"
							+ tempAttachmentStringList.getFirst()[1] + "^\" ";
					tempAttachmentStringList.removeFirst();
				}
			}
			// MKVTool command --ui-language zh_TW/en
			mkvToolCommand = "mkvmerge --output ^\"" + outputPath + filename + ".mkv^\" --no-attachments "
			// Input video
					+ "^\"^(^\" ^\"" + inputPath + "\\" + filename + "." + videoExtension + "^\" ^\"^)^\" "
					// Input subtitle(if any)
					+ subtitleString
					// Input image
					+ "--attachment-name cover." + imageExtension+ " --attach-file ^\""
					+ inputPath + "\\" + filename + "." + imageExtension + "^\" "
					// Input attachment(if any)
					+ attachmentString
					// Track order
					+ "--track-order " + trackOrderString;
			// System.out.println("mkvToolCommand: " + mkvToolCommand);
			// Run cmd
			try {
				ProcessBuilder builder = new ProcessBuilder("cmd.exe", "/c", mkvToolCommand);
				builder.redirectErrorStream(true);
				Process p = builder.start();
				BufferedReader r = new BufferedReader(new InputStreamReader(p.getInputStream(), "UTF-8"));
				String line;
				while (true) {
					line = r.readLine();
					if (line == null) {
						break;
					}
					System.out.println(line);
				}
				mkvmergeExitCode = p.exitValue();
			} catch (IOException ioe) {
				System.out.println("\nIOException occurred when merging, program ended");
				System.exit(0);
			} finally {
				if (mkvmergeExitCode == 0 || mkvmergeExitCode == 1) {
					if (moveToTrash) {
						// Delete video file
						String tempFilename = filename.replace("^&", "&");
						try {
							System.out.println("\nMoving \"" + inputPath + "\\"
									+ tempFilename + "." + videoExtension + "\" to the Recycle Bin");
							boolean tempBoolean = Desktop.getDesktop().moveToTrash(Path.of(
									inputPath + "\\" + tempFilename + "." + videoExtension).toFile());
							if (!tempBoolean)
								System.out.println("Unable to delete file \""
										+ inputPath + "\\" + tempFilename + "." + videoExtension);
						} catch (SecurityException se) {
							System.out.println("\nUnable to delete file \"" + inputPath + "\\"
									+ tempFilename + "." + videoExtension + "\" due to SecurityException");
						} catch (UnsupportedOperationException uoe) {
							System.out.println("\nUnable to delete file \"" + inputPath + "\\"
									+ tempFilename + "." + videoExtension + "\" due to UnsupportedOperationException");
						} catch (NullPointerException npe) {
							System.out.println("\nUnable to delete file \"" + inputPath + "\\"
									+ tempFilename + "." + videoExtension + "\" due to NullPointerException");
						} catch (IllegalArgumentException iae) {
							System.out.println("\nUnable to delete file \"" + inputPath + "\\"
									+ tempFilename + "." + videoExtension + "\" due to IllegalArgumentException");
						}
						// Delete image file
						try {
							System.out.println("Moving \"" + inputPath + "\\"
									+ tempFilename + "." + imageExtension + "\" to the Recycle Bin");
							boolean tempBoolean = Desktop.getDesktop().moveToTrash(Path.of(
									inputPath + "\\" + tempFilename + "." + imageExtension).toFile());
							if (!tempBoolean)
								System.out.println("Unable to delete file \""
										+ inputPath + "\\" + tempFilename + "." + imageExtension);
						} catch (SecurityException se) {
							System.out.println("\nUnable to delete file \"" + inputPath + "\\"
									+ tempFilename + "." + imageExtension + "\" due to SecurityException");
						} catch (UnsupportedOperationException uoe) {
							System.out.println("\nUnable to delete file \"" + inputPath + "\\"
									+ tempFilename + "." + imageExtension + "\" due to UnsupportedOperationException");
						} catch (NullPointerException npe) {
							System.out.println("\nUnable to delete file \"" + inputPath + "\\"
									+ tempFilename + "." + imageExtension + "\" due to NullPointerException");
						} catch (IllegalArgumentException iae) {
							System.out.println("\nUnable to delete file \"" + inputPath + "\\"
									+ tempFilename + "." + imageExtension + "\" due to IllegalArgumentException");
						}
						// Delete subtitle file(s)
						for (String[] subtitleArray : subtitleStringList) {
							String tempSubtitleFile = subtitleArray[1].replace("^&", "&");
							if (filename == subtitleArray[0]) {
								try {
									System.out.println("Moving \"" + inputPath + "\\"
											+ tempSubtitleFile + "\" to the Recycle Bin");
									boolean tempBoolean = Desktop.getDesktop().moveToTrash(Path.of(
											inputPath + "\\" + tempSubtitleFile).toFile());
									if (!tempBoolean)
										System.out.println("Unable to delete file \""
												+ inputPath + "\\" + tempSubtitleFile);
								} catch (SecurityException se) {
									System.out.println("\nUnable to delete file \"" + inputPath + "\\"
											+ tempSubtitleFile + "\" due to SecurityException");
								} catch (UnsupportedOperationException uoe) {
									System.out.println("\nUnable to delete file \"" + inputPath + "\\"
											+ tempSubtitleFile + "\" due to UnsupportedOperationException");
								} catch (NullPointerException npe) {
									System.out.println("\nUnable to delete file \"" + inputPath + "\\"
											+ tempSubtitleFile + "\" due to NullPointerException");
								} catch (IllegalArgumentException iae) {
									System.out.println("\nUnable to delete file \"" + inputPath + "\\"
											+ tempSubtitleFile + "\" due to IllegalArgumentException");
								}
							}
						}
						// Delete attachment file(s)
						for (String[] attachmentArray : attachmentStringList) {
							String tempAttachmentFile = attachmentArray[1].replace("^&", "&");
							if (filename == attachmentArray[0]) {
								try {
									System.out.println("Moving \"" + inputPath + "\\"
											+ tempAttachmentFile + "\" to the Recycle Bin");
									boolean tempBoolean = Desktop.getDesktop().moveToTrash(Path.of(
											inputPath + "\\" + tempAttachmentFile).toFile());
									if (!tempBoolean)
										System.out.println("Unable to delete file \""
												+ inputPath + "\\" + tempAttachmentFile);
								} catch (SecurityException se) {
									System.out.println("\nUnable to delete file \"" + inputPath + "\\"
											+ tempAttachmentFile + "\" due to SecurityException");
								} catch (UnsupportedOperationException uoe) {
									System.out.println("\nUnable to delete file \"" + inputPath + "\\"
											+ tempAttachmentFile + "\" due to UnsupportedOperationException");
								} catch (NullPointerException npe) {
									System.out.println("\nUnable to delete file \"" + inputPath + "\\"
											+ tempAttachmentFile + "\" due to NullPointerException");
								} catch (IllegalArgumentException iae) {
									System.out.println("\nUnable to delete file \"" + inputPath + "\\"
											+ tempAttachmentFile + "\" due to IllegalArgumentException");
								}
							}
						}
					}
					if (mkvmergeExitCode == 1) {
						System.out.println(
								"\nWarning occurred, check both the warning and the resulting file is recommended");
						warningNum++;
					} else
						completedNum++;
				} else if (mkvmergeExitCode == 2) {
					System.out.println("\nError occurred, mission aborted");
					abortNum++;
				} else
					System.out.println("\nUnknown exit code: " + mkvmergeExitCode);
				// Remove completed file from list
				filenames.removeFirst();
				if (!filenames.isEmpty())
					System.out.println("\n" + filenames.size() + " file(s) remaining\n");
				else
					System.out.println("\nMerge process ended with " + completedNum + " video completed, "
							+ warningNum + " warning, " + abortNum + " error");
			}
		} while (!filenames.isEmpty());
		scanner1.close();
	}
}