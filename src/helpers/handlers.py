from utils.logger import SyncLogger
import streamlit as st
import pyperclip


class HumanizerHandlers:

    def __init__(self, gemini_api_key: str) -> None:
        """
        Initialize the HumanizerHandlers class.
        This class contains methods to handle user interactions in the Streamlit app.

        Args:
            gemini_api_key (str): The Google Gemini API key.
        """
        self.api_key = gemini_api_key
        self.logger = SyncLogger("HumanizerHandlers")


    def handle_clipboard_paste(self) -> None:
        """
        Handle the paste button click event.
        This method pastes the content from the clipboard into the input text area.
        """
        try:
            if not self.api_key:
                st.toast("Please enter your Google Gemini API key.", icon="⚠️")
                self.logger.write_log("error", "Paste button clicked without API key")
                return

            st.session_state.input = pyperclip.paste()
            st.session_state.output = ""
            self.logger.write_log("info", "Pasted text from clipboard")
        except Exception as e:
            self.logger.write_log("error", f"Failed to paste from clipboard: {e}")
            st.toast("Unable to access clipboard. Please paste manually.", icon="❌")


    def clear_text(self) -> None:
        """
        Clear the input and output text areas.
        This method resets the input and output text areas to empty strings.
        """
        try:
            if not self.api_key :
                st.toast("Please enter your Google Gemini API key.", icon="⚠️")
                self.logger.write_log("error", "Clear button clicked without API key")
                return

            st.session_state.input = ""
            st.session_state.output = ""
            self.logger.write_log("info", "Cleared input and output text areas")
        except Exception as e:
            self.logger.write_log("error", f"Failed to clear text: {e}")
            st.toast("Unable to clear text.", icon="❌")


    def copy_to_clipboard(self) -> None:
        """
        Copy the output text to the clipboard.
        This method copies the content of the output text area to the clipboard.
        """
        try:
            if not self.api_key:
                st.toast("Please enter your Google Gemini API key.", icon="⚠️")
                self.logger.write_log("error", "Copy to clipboard clicked without API key")
                return

            pyperclip.copy(st.session_state.output)
            st.toast("Copied to clipboard!", icon="✅")
            self.logger.write_log("info", "Copied output to clipboard")
        except Exception as e:
            self.logger.write_log("error", f"Failed to copy to clipboard: {e}")
            st.toast("Unable to copy to clipboard. Please copy manually.", icon="❌")


    def on_humanize_click(self) -> None:
        """
        Handle the click event for the humanize button.
        """
        try:
            if not self.api_key:
                st.toast("Please enter your Google Gemini API key.", icon="⚠️")
                self.logger.write_log("error", "Humanize button clicked without API key")
                return

            if st.session_state.input.strip():
                st.session_state.humanize_clicked = True
                self.logger.write_log("info", "Humanize button clicked")
            else:
                st.toast("Please enter some text to humanize.", icon="❌")
                self.logger.write_log("error", "Humanize button clicked with empty input")
        except Exception as e:
            self.logger.write_log("error", f"Error in humanize button click: {e}")
            st.toast("An error occurred while processing your request.", icon="❌")
