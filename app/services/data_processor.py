import pandas as pd
from app.models.base import Sales
from fastapi import HTTPException, status

async def process_sales_data(file, db):

    df = pd.read_csv(file)

    # 1️⃣ Clean column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(r"\s+", "_", regex=True)
    )

    # 2️⃣ Required columns (quantity removed)
    required_columns = [
        'date',
        'product_name',
        'selling_price',
        'category'
    ]

    missing_cols = [col for col in required_columns if col not in df.columns]

    if missing_cols:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"CSV is missing required columns: {', '.join(missing_cols)}"
        )

    # 3️⃣ Handle optional quantity
    if 'quantity' not in df.columns:
        df['quantity'] = 1

    df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce').fillna(1).astype(int)

    # 4️⃣ Remove extra columns
    allowed_columns = required_columns + ['quantity']
    df = df[allowed_columns]
    print("all columns after processing:", df.columns.tolist())
    df['date'] = df['date'].astype(str).str.strip()

    try:
        df['date'] = pd.to_datetime(df['date'],format="%d-%m-%Y").dt.date
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Date format should be DD-MM-YYYY")

    # 6️⃣ Insert into DB
    sales_objects = [
        Sales(
            product_name=row['product_name'],
            quantity=row['quantity'],
            selling_price=row['selling_price'],
            category=row['category'],
            date=row['date']
        )
        for _, row in df.iterrows()
    ]

    db.add_all(sales_objects)
    await db.commit()

    return {"message": "Upload successful"}
# This is data processor