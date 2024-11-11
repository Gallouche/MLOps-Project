# MLOps project

## Installation

### Option 1: Install with Flexible Dependencies

This method installs the project using the dependencies specified in `pyproject.toml`, allowing `pip` to resolve the latest compatible versions.

1. **Clone the Repository**:
2. **Install the requirements**:

   ```bash
   pip install .
   ```

### Option 2: Install with Exact Versions (Recommended for Production)

For a consistent environment with exact dependency versions, use the `requirements.txt` file.

1. **Install from `requirements.txt`**:

   ```bash
   pip install -r requirements.txt
   ```

## Adding Dependencies

To add or update dependencies in your project, follow these steps:

1. **Edit `pyproject.toml`**:
   Open the `pyproject.toml` file and add the new dependency under the `dependencies` section. For example:

   ```toml
   [project]
   dependencies = [
       "numpy>=1.21.0",
       "pandas>=1.3.0",
       "new-package>=1.0.0"
   ]
   ```

2. **Install the New Dependency**:
   Run the following command to install the new or updated dependency:

   ```bash
   pip install .
   ```

3. **Update `requirements.txt`** (Optional but Recommended):
   To lock the current versions of all dependencies for consistency, update `requirements.txt` by running:

   ```bash
   pip freeze > requirements.txt
   ```

## Data

https://www.mapillary.com/datasets

## Presentation on Airflow

https://docs.google.com/presentation/d/1-wukqNc3vpEbHzBJVt9H14qNZzdjb8Dl9J3qQs1SSvE/edit?usp=sharing
