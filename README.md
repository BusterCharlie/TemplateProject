# TemplateProject

A GUI-based Python project generator for quickly creating new applications, powered by `ttkbootstrap`.

This tool was created to streamline the process of starting a Python project with a simple GUI. It sets up a clean project structure, a virtual environment, and includes a theme engine out of the box, so you can focus on building your app's features.

<a href="https://github.com/user-attachments/assets/1a37cc68-3c06-41f7-b7d8-ddebda008f99">
  <img width="400" alt="TemplateProject Generator" src="https://github.com/user-attachments/assets/1a37cc68-3c06-41f7-b7d8-ddebda008f99" />
</a>


## Features

-   **Easy-to-Use GUI**: Configure your new project through a simple and intuitive interface.
-   **Comprehensive Project Setup**:
    -   Define your project's name, description, and output directory.
    -   Include author information (name and email) which is automatically added to the `pyproject.toml` and `LICENSE` files.
-   **Customization**:
    -   **Icon Support**: Automatically convert an image (`.png`, `.jpg`, etc.) into a `.ico` file for your application's icon.
    -   **Theme Engine**: Select from various light and dark themes from `ttkbootstrap`. The generated project includes the same theme selection capability, and remembers your choice.
-   **Technical Foundation**:
    -   **Python Version**: Choose the target Python version for your project (supports 3.9 - 3.12).
    -   **Virtual Environment**: Automatically creates a Python virtual environment using `uv` for fast and reliable dependency management.
    -   **Git Initialization**: Initializes a new Git repository in your project folder by default (this can be disabled).
-   **Complete Project Template**:
    -   A well-organized directory structure.
    -   `pyproject.toml` pre-configured with necessary dependencies like `ttkbootstrap`.
    -   A professional `README.md` template.
    -   Cross-platform run scripts (`run.bat` for Windows, `run.sh` for Unix-like systems).
    -   Standard `.gitignore` and `LICENSE` files.
-   **Configuration Persistence**: All settings, including output path, author info, and theme selection, are saved to a local config file. Your preferences are remembered for the next time you run the generator.

## How to Use

1.  Run the `TemplateProject` application. (you should be able to use `run.bat` for Windows, `run.sh` for Unix-like systems).
2.  On the **Home** tab, fill in your project details:
    -   **Project Name**: A name for your project (e.g., `MyCoolApp`). It's best to use a name that is friendly for folder and repository naming.
    -   **Project Description**: A short description for your `README.md`.
    -   **Project Directory**: The parent folder where your new project folder will be created.
    -   **Icon Path (Optional)**: Path to an image to use as the app icon.
    -   **Author Name & Email (Optional)**: For the `pyproject.toml` and `LICENSE` files.

3.  Switch to the **Settings** tab to configure the environment:
    -   Select the desired **Python Version**.
    -   Toggle **Initialize Git Repository** if needed.
    -   You can also change the theme of the generator app itself.
    -   

    <a href="https://github.com/user-attachments/assets/d8c519cd-0ee5-4c2f-be9a-ec01286f9d64">
      <img width="400" alt="Settings Tab" src="https://github.com/user-attachments/assets/d8c519cd-0ee5-4c2f-be9a-ec01286f9d64" />
    </a>

4.  Click **Generate Project**. A confirmation will appear once it's done.

    <a href="https://github.com/user-attachments/assets/e01c4b8b-aa91-4e35-9ad8-d0081777ba38">
      <img width="214" height="150" alt="Confirmation Dialog" src="https://github.com/user-attachments/assets/e01c4b8b-aa91-4e35-9ad8-d0081777ba38" />
    </a>

5.  That's it! Your new project is ready for you to start coding.

## The Generated Project

Your new project is created with a clean, ready-to-use structure. It includes a sample application window with "Home" and "Settings" tabs.

-   The **Home** tab is where you'll add your application's main functionality.
-   The **Settings** tab comes with the same theme selector, allowing users of your app to change its appearance. The chosen theme is saved and reapplied on the next launch.

<a href="https://github.com/user-attachments/assets/0ed9ae59-abd4-42ea-a008-5345a9ab11d3">
  <img width="400" alt="Generated Project Home Tab" src="https://github.com/user-attachments/assets/0ed9ae59-abd4-42ea-a008-5345a9ab11d3" />
</a>
<br/>
<a href="https://github.com/user-attachments/assets/472497e2-33e7-4915-a57a-1f411e9150d2">
  <img width="400" alt="Generated Project Settings Tab" src="https://github.com/user-attachments/assets/472497e2-33e7-4915-a57a-1f411e9150d2" />
</a>

## Requirements

-   Python 3.9+ to run the generator.
-   The `run` scripts will automatically handle the installation of `uv` and other dependencies into a local virtual environment.

## License

This project is licensed under the MIT License. The generated projects also include an MIT License by default.

