package_weight_check_button_style = """
            QPushButton {
                background-color: #ff661a;
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #e55414;
            }
            QPushButton:pressed {
                background-color: #c44712;
            }
        """

upload_button_style = """
            QPushButton {
                background-color: #ff661a;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 5px;
                padding: 3px
            }
            QPushButton:hover {
                background-color: #e55414;
            }
            QPushButton:pressed {
                background-color: #c44712;
            }
        """

upload_button_styleResize =  """
            QPushButton {
                background-color: #E84545;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 5px;
                padding: 3px
            }
            QPushButton:hover {
                background-color: #E84545;
            }
            QPushButton:pressed {
                background-color: #E84545;
            }
        """

resize_button = """
            QPushButton {
                background-color: #E84545;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #D93C3C;
            }
            QPushButton:pressed {
                background-color: #C43131;
            }
        """


# Header Style
header_style = """
    QLabel {
        background-color: #242424;
        color: #00ADB5;
        font-size: 24px;
        font-weight: bold;
        padding: 10px 0;
        border-bottom: 1px solid #00ADB5;
    }
"""

# Footer Style
footer_style = """
    QLabel {
        background-color: #2f2f2f;
        color: #A0A0A0;
        font-size: 12px;
        padding: 10px 0;
        border-top: 1px solid #00ADB5;
    }
"""

# Input Style
input_style = """
    QLineEdit {
        background-color: #f5f5f5;
        border: 1px solid #B0B0B0;
        border-radius: 8px;
        padding: 10px;
        color: #333;
        font-size: 14px;
    }

    QLineEdit:focus {
        border-color: #00ADB5;
    }
"""

# ComboBox Style
combo_box_style = """
    QComboBox {
        background-color: #f5f5f5;
        border: 1px solid #B0B0B0;
        border-radius: 8px;
        padding: 8px;
        color: #333;
        font-size: 14px;
    }

    QComboBox:focus {
        border-color: #00ADB5;
    }
"""

# Button Style (with hover and pressed states)
button_style = """
    QPushButton {
        background-color: #00ADB5;
        color: white;
        font-size: 14px;
        font-weight: bold;
        border-radius: 5px;
        padding: 12px 24px;
        border: none;
    }

    QPushButton:hover {
        background-color: #009A9C;
    }

    QPushButton:pressed {
        background-color: #007B7C;
    }
"""

# Button Style for "Run Script" and "Generate File"
run_button_style = """
    QPushButton {
        background-color: #00ADB5;
        color: white;
        font-size: 14px;
        font-weight: bold;
        border-radius: 5px;
        padding: 12px 24px;
        border: none;
    }

    QPushButton:hover {
        background-color: #009A9C;
    }

    QPushButton:pressed {
        background-color: #007B7C;
    }
    QPushButton:disabled {
        background-color: #aaaaaa;
        color: #666666;
        border: none;
    }

"""

# Button Style for Resize Button
resize_button_style = """
    QPushButton {
        background-color: #E84545;
        color: white;
        font-size: 16px;
        font-weight: bold;
        border-radius: 5px;
        padding: 10px 20px;
        border: none;
    }

    QPushButton:hover {
        background-color: #D93C3C;
    }

    QPushButton:pressed {
        background-color: #C43131;
    }
"""

run_button_styleT = """
    QPushButton {
        background-color: #4287f5; /* Blue color */
        color: white;
        font-size: 14px;
        font-weight: bold;
        border-radius: 5px;
        padding: 12px 24px;
        border: none;
    }

    QPushButton:hover {
        background-color: #306ecc; /* Darker blue for hover */
    }

    QPushButton:pressed {
        background-color: #244b8a; /* Even darker blue for pressed */
    }

    QPushButton:disabled {
        background-color: #d0d7e3; /* Light grey-blue for disabled */
        color: #666666;
        border: none;
    }
"""
window_style = """
    QWidget {
        background-color: #1E1E1E;
    }
"""