# Customer ORM

A Python customer-management project using SQLAlchemy ORM, with customer, payment, mobile-number, Adeona table, and SMS message-classification functionality.

## Features

- Customer records managed through the customer model and controller.
- Payment-related records and ORM relationships.
- Salary-related database schema in `salary.sql`.
- SMS classification into Transactional or Promotional using the model assets in `ml_models/`.
- Database setup in `config/database.py`.
- Shared validation utilities in `utils/validation.py`.

## SMS Classification Labels

| Label | Meaning |
|---|---|
| `0` | Transactional |
| `1` | Promotional |

Keep the label mapping consistent with `ml_models/label_map.json`.

## Project Structure

```text
CUSTOMER_ORM/
├── config/
│   └── database.py
├── controllers/
│   ├── adeona_controller.py
│   ├── customer_controller.py
│   ├── message_controller.py
│   ├── mobile_controllers.py
│   └── payment_controller.py
├── ml_models/
│   ├── config.json
│   ├── label_map.json
│   ├── model.safetensors
│   ├── tokenizer_config.json
│   └── tokenizer.json
├── models/
│   ├── adeona_tables_model.py
│   ├── customer_model.py
│   ├── message_models.py
│   ├── mobile_model.py
│   └── payment_model.py
├── utils/
│   ├── ml_manager.py
│   └── validation.py
├── .env                  # local only; do not commit
├── .gitignore
├── adeonaTable.sql
├── app.py
├── customers.sql
├── message_new.sql
├── message.sql
├── mobile_number.sql
├── payments.sql
├── salary.sql
└── test_db.py
```

Generated `__pycache__/` folders and the local `.venv/` environment should not be committed.

## Technology

- Python
- SQLAlchemy ORM
- Database configured in `config/database.py`
- Model and tokenizer assets stored in `ml_models/`

Confirm the exact database engine, database driver, and ML libraries from the source imports.

## Setup

This repository does not need a `requirements.txt` if you prefer to install dependencies directly. Install the third-party packages imported by the project in your own virtual environment.

### 1. Clone the repository

```bash
git clone https://github.com/<YOUR-GITHUB-USERNAME>/CUSTOMER_ORM.git
cd CUSTOMER_ORM
```

### 2. Create and activate a virtual environment (Windows PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

Install SQLAlchemy and the database driver required by `config/database.py`. If `utils/ml_manager.py` uses libraries such as Transformers and PyTorch, install those as well.

Example for SQLAlchemy only:

```powershell
python -m pip install sqlalchemy
```

This is not the complete dependency list for the application. Check imports in `app.py`, `config/`, `controllers/`, `models/`, and `utils/` and install the corresponding packages.

### 4. Configure the database

Create a local `.env` file with the environment variables expected by `config/database.py`. Never commit your real `.env` file. You may provide a `.env.example` with placeholder values only.

### 5. Prepare the database

Review the SQL files and execute the required schema files in the correct order for your database engine. Check them for real customer, payment, salary, or other sensitive data before publishing.

### 6. Run

If these files are designed to be executed directly:

```powershell
python app.py
python test_db.py
```

Run `test_db.py` separately when testing the database.

## Model Files and GitHub File Limits

The classifier's assets are stored in `ml_models/`. Check the size of `model.safetensors` before pushing. GitHub blocks ordinary Git files larger than 100 MB. If the model exceeds that limit, use Git LFS or host the model separately and document how to obtain it. Keep all required model/tokenizer assets accessible if classification needs to run after cloning.

## Security and Privacy

- Never commit `.env`, passwords, database URLs containing credentials, API keys, or access tokens.
- Do not publish real customer details, phone numbers, payment records, salary records, database dumps, or private datasets.
- SQL files should contain schema or safe sample data only.
- Use synthetic or anonymized data for demos.
- Restrict access to payment and salary information in deployed environments.

## Testing

Use `test_db.py` according to its implementation to verify database connectivity or database behavior. Also test customer operations, payment handling, mobile-number handling, and both SMS classification labels.

## License

Add a license only if you intend to grant others specific reuse rights.
