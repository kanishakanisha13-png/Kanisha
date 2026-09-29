from backend.gemini_utils import generate_recommendation
from backend.database import get_connection


def create_recommendation(
    category: str,
    budget: float,
    preferences: str = "",
    user_id: int | None = None
) -> str:

    prompt = f"""
You are PocketSmart AI, a smart budget and recommendation assistant.

Category: {category}
Budget: ₹{budget}
User preferences: {preferences}

Provide practical recommendations that stay within the given budget.

For each recommendation, include:
- Product or service idea
- Estimated price
- Short reason
- Platform/source suggestion

Keep the response clear and easy to understand.
"""

    recommendation = generate_recommendation(prompt)

    # Save recommendation to SQLite database
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO recommendation_history
        (user_id, category, budget, preferences, recommendations)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            user_id,
            category,
            budget,
            preferences,
            recommendation
        )
    )

    connection.commit()
    connection.close()

    return recommendation


def get_recommendation_history(user_id: int | None = None):

    connection = get_connection()
    cursor = connection.cursor()

    if user_id is not None:

        cursor.execute(
            """
            SELECT
                id,
                category,
                budget,
                preferences,
                recommendations
            FROM recommendation_history
            WHERE user_id = ?
            ORDER BY id DESC
            """,
            (user_id,)
        )

    else:

        cursor.execute(
            """
            SELECT
                id,
                category,
                budget,
                preferences,
                recommendations
            FROM recommendation_history
            ORDER BY id DESC
            """
        )

    history = cursor.fetchall()

    connection.close()

    return [dict(row) for row in history]