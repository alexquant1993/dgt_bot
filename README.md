# Project Title

This project is a Python application that interacts with a website to detect the availability of DGT appointments and solves CAPTCHAs using the 2Captcha service and selenium_recaptcha_solver.

## Dependencies

This project uses the following Python libraries:

- `selenium`: For automating web browser interaction.
- `twocaptcha`: For solving CAPTCHAs using the 2Captcha service.

## How It Works

The application navigates to a website, finds the CAPTCHA on the page, and sends it to the 2Captcha service to be solved. The solved CAPTCHA is then inputted back into the page.

The application can handle both reCAPTCHA v2 and v3. For reCAPTCHA v2, it finds the CAPTCHA iframe on the page and clicks on it. For reCAPTCHA v3, it inputs the solved CAPTCHA response into a textarea on the page.

## Usage

To use this application, you need to provide your 2Captcha API key and the site key for the website you're interacting with. These should be set as the `TWO_CAPTCHA_API_KEY` and `SITE_KEY` attributes of the `DGTBot` class, respectively.

You also need to replace `'submit-button-id'` with the actual ID of the submit button on your webpage in the `solve_captcha` method.

## Note

This is a basic description based on the provided code. For more detailed information, please refer to the comments in the `main.py` file.