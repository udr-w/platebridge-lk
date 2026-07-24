# Localisation review

English, Sinhala and Tamil interface resources live in `frontend/src/locales`. The selected locale persists and updates the HTML `lang` attribute. The translations are conservative prototype copy and require native-speaker and community review.

| Key | English | Sinhala | Tamil | Review note |
|---|---|---|---|---|
| tagline | Good food deserves another table, not a garbage bin. | හොඳ ආහාර කුණු බඳුනට නොව, තවත් කෑම මේසයකට යා යුතුයි. | நல்ல உணவு குப்பைக்குச் செல்லாமல், இன்னொரு உணவு மேசையைச் சென்றடைய வேண்டும். | High confidence; review cadence/naturalness |
| recipient | Recipient | ලබන්නා | பெறுநர் | Neutral but community testing needed |
| food rescue | Food rescue | ආහාර ගලවාගැනීම | உணவு மீட்பு | Check sector-preferred terminology |
| coordinator review | Coordinator review required | සම්බන්ධීකාරක සමාලෝචනය අවශ්‍යයි | ஒருங்கிணைப்பாளர் ஆய்வு தேவை | Operational meaning is clear |
| public alias | Public alias | පොදු අන්වර්ථ නාමය | பொது மாற்றுப்பெயர் | Review privacy comprehension |
| not eligible | Not eligible for redistribution | නැවත බෙදාහැරීමට සුදුසු නැත | மறுவிநியோகத்துக்குத் தகுதியற்றது | Avoids claiming “unsafe” diagnosis |
| incident | Issue/incident | ගැටලුව | சிக்கல் | Simplified for understandable UI |

Long dynamic food descriptions remain seeded English content; a pilot should support translated donor content or coordinator-assisted summaries. Dates use the browser locale but have not been redesigned for every local convention.

