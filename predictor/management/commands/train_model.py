import joblib
import pandas as pd
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

class Command(BaseCommand):
    help = "Train a regression model from a CSV of historical student outcomes."

    def add_arguments(self, parser):
        parser.add_argument("--csv", required=True, help="CSV path with attendance, unit_tests, assignments, classwork, final_score")

    def handle(self, *args, **options):
        path = Path(options["csv"])
        if not path.exists():
            raise CommandError(f"CSV file not found: {path}")
        df = pd.read_csv(path)
        features = ["attendance", "unit_tests", "assignments", "classwork"]
        target = "final_score"
        missing = [c for c in features + [target] if c not in df.columns]
        if missing:
            raise CommandError("Missing required CSV columns: " + ", ".join(missing))
        df = df[features + [target]].apply(pd.to_numeric, errors="coerce").dropna()
        if len(df) < 10:
            raise CommandError("Provide at least 10 complete historical rows; more data is strongly recommended.")
        if (df[features + [target]] < 0).any().any() or (df[features + [target]] > 100).any().any():
            raise CommandError("All scores must be between 0 and 100.")
        X, y = df[features], df[target]
        if len(df) >= 20:
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        else:
            X_train, X_test, y_train, y_test = X, X, y, y
        model = RandomForestRegressor(n_estimators=200, random_state=42, min_samples_leaf=2)
        model.fit(X_train, y_train)
        pred = model.predict(X_test)
        self.stdout.write(f"Validation MAE: {mean_absolute_error(y_test, pred):.2f}")
        if len(y_test) > 1:
            self.stdout.write(f"Validation R²: {r2_score(y_test, pred):.3f}")
        out = Path(settings.BASE_DIR) / "predictor" / "grade_model.joblib"
        joblib.dump(model, out)
        self.stdout.write(self.style.SUCCESS(f"Saved model to {out}"))
        self.stdout.write("Evaluate on a separate held-out cohort before relying on predictions.")
