import logging
import os


def generate_real_estate_listings(config, ai_client):
    """Generates Real Estate listings using AI and saves the results as a JSON object to a local file.
    If the file already exists, this function does nothing."""

    if os.path.exists(config.real_estate_listings_path):
        logging.info(f'Skipping generation of "{config.real_estate_listings_path}" as it already exists.')
        return

    logging.info(f'Generating "{config.real_estate_listings_path}"...')

    system_prompt = """\
You are a professional data generator that creates realistic but entirely fictional real estate data for testing and prototyping purposes.

Guidelines:
- Always produce strictly valid JSON output — no extra commentary, text, or Markdown formatting.
- All listings must be fictional; never use real addresses, people, or identifiable information.
- Ensure diversity across property types, price ranges, neighborhoods, and styles.
- Include a wide variety of locations, such as beach, forest, mountains, small town, capital city, etc.
- Keep all numeric values internally consistent (e.g., higher price for larger or more luxurious homes).
- Descriptions should sound natural and believable, written in 3–5 sentences, highlighting key features and lifestyle appeal.
- Avoid repetition or identical phrasing between listings.
- Do not include any null or placeholder values.
"""

    logging.debug("--- Real Estate Listings System Prompt ---")
    logging.debug(system_prompt)

    user_prompt = """\
Generate 20 diverse real estate listings.

Each listing must be in the following JSON format:
{
  "price": <integer>,
  "neighborhood": <string>,
  "property_type": <string>,
  "bedrooms": <integer>,
  "bathrooms": <integer>,
  "area_sqft": <integer>,
  "description": <3-5 sentences>
}

Return ONLY valid JSON structured as:
{
  "listings": [ ... ]
}
"""

    logging.debug("--- Real Estate Listings User Prompt ---")
    logging.debug(user_prompt)

    response = ai_client.chat.completions.create(
        model="gpt-5",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
    )

    with open(config.real_estate_listings_path, 'w') as file:
        file.write(response.choices[0].message.content)


def generate_home_recommendation(user_input, relevant_listings, ai_client):
    """Generates a personalised home recommendation using AI based on the user's input and
    relevant real estate listings extracted from a ChromaDB vector search."""

    system_prompt = """\
You are an expert real estate copywriter who creates engaging, personalized property descriptions 
that highlight why a home is a great fit for a particular buyer.

Guidelines:
- Read the buyer’s stated preferences and the top 3 relevant property listings provided.
- Write 1–2 short paragraphs that describe the listings most suited to this buyer.
- If any listings clearly do not align with the buyer’s preferences, **exclude them**.
- Focus on emphasizing the features and lifestyle benefits that match what the buyer is looking for.
- Keep all factual information accurate — do not invent or alter details like location, size, or features.
- Make the writing warm, vivid, and appealing, but natural and credible — similar to professional real estate marketing copy.
- Avoid repetitive phrasing or listing-style descriptions. 
"""

    logging.debug("--- Home Recommendation System Prompt ---")
    logging.debug(system_prompt)

    user_prompt = f"""\
Generate a personalized property description for a home using the buyer preferences and relevant listings.

Buyer Preferences:
{user_input}

Relevant Listings (top 3 from vector search):
{"\n---\n".join(relevant_listings["documents"][0])}
"""

    logging.debug("--- Home Recommendation User Prompt ---")
    logging.debug(user_prompt)

    response = ai_client.chat.completions.create(
        model="gpt-5",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
    )

    return response.choices[0].message.content
