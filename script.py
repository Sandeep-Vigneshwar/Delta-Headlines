import ollama
import re

def clean_summary(summary):
    summary = summary.strip()
    if not summary.endswith((".", "!", "?")):
        summary += "."
    summary = re.sub(r"\s+", " ", summary)
    return summary

def generate_military_script(summary, retries=3):
    summary = clean_summary(summary)
    if len(summary.split()) < 5:
        return "ERROR: The provided summary is too short or incomplete for a proper report."
    prompt = f"""
    You are a military news reader delivering a report. Convert the following news summary into a professional, authoritative script with a commanding tone. Use military-style phrases where appropriate.
    Summary:
    {summary}
    Format:
    - Open with a strong introduction
    - Deliver key facts with confidence
    - End with a professional sign-off
    Example Sign-off: "This is team tech twins, reporting for Delta Defense Network."
    """

    for attempt in range(retries):
        try:
            response = ollama.chat(model="nemotron-mini:latest", messages=[{"role": "user", "content": prompt}])
            return response['message']['content']
        except Exception as e:
            print(f"Attempt {attempt+1} failed: {e}")

    return "ERROR: Failed to generate the military script after multiple attempts."

summary_text = '''Bangladesh crisis offers
new opportunities for
Indian textile clusters
Ravi outta Mishra
New Delhi January 5
amid the ongoing economic and political tensions in
Bangladesh, Indian exporting
firms, particularly in the
Tirupur clusters, are receiving
higher inquiries from several
global apparel brands, including Primark Tesco, decathlon,
duns c Penney gap next and
Walmart, with order conversion expected for shipment by
early 2025, MIT hi less war
Shakur, secretary general of
the apparel export promotion
council(an etc) said.
Due to a record surge in the
US dollar's value, Bangladesh
has faced a sharp depletion in
its foreign exchange reserves,
which fell below 40 billion for
the first time in two years in
July last year. With foreign
exchange reserves sufficient to
cover only four to five months
of imports, Bangladesh has
faced challenges in importing
cotton and fabric, which it traditionally sources from India.
This comes amid tightening
economic conditions in the
neighboring country.
" This crisis also presents an
opportunity for additional
employment generation. Capturing just 10 percent of
bangladesh's global apparel
exports could directly create
5, 00, o00 jobs and indirectly
generate an additional 1 million jobs in the Indian apparel
sector. To seize the opportunity
presented by this development, India needs to urgently
address issues related to capacity augmentation and skill
development," Shakur said.
Most European brands sourcing from Bangladesh, particularly in the cost-sensitive segment, are facing challenges in
immediately shifting orders to
alternative destinations, due to
the distinct cost advantages
offered by the country, such as
low wage rates, duty-free
financial express

Mit hi less war Shakur
access, and its least developed
country LDC) status. However, several prominent brands
have decided not to further
increase their exposure to
Bangladesh for sourcing,
Shakur added.
Bangladesh enjoys a 10–15 percent cost advantage over India,
as its apparel products benefit
from duty-free access in the
European Union, the UK, and
Canada due to its LDC status.
India can only bridge the
duty disadvantage after it
signs a free trade agreement
with the EU and the UK. currently, several Indian manufacturers have set up factories
in Bangladesh due to india's
labor laws, concerns about
unions, and the cost disadvantage. Thakur further said that
global investments are driven
by the political stability index,
and the continued instability
in Bangladesh presents a significant opportunity for India
to attract investments that
might otherwise flow to neighbor ring competing countries
such as Vietnam, Cambodia,
and Indonesia." however, with
a strong focus on improving
and upgrading infrastructure,
capacity expansion, technology infusion, and compliance,
mon06 January 2025
https:// paper. Financial express. Com/ c/ 7656426

India is well-positioned to cap
it alive on these redirected
investments. We are also in
talks with agencies and consulting firms to engage them
in improving productivity and
efficiency in the operations of
garment manufacturing companies, which can unlock the
capacity in the apparel sector,"
Shakur said.
On pli2. 0:
and seize the opportunities
arising from the reorientation
of supply chains due to
bangladesh's crisis and the
china+ 1 factor, India must act
swiftly to enhance its production capacity, shorten production cycle times, and improve
speed to market, in addition to
focusing on workforce training
and developing a robust compliance architecture, Shakur
said. Accordingly, the pli2. 0
scheme for all types of garments, irrespective of fiber,
with a reduced investment
threshold, should be introduced on an urgent basis. This
scheme would foster investment and scale up production
capacity exponentially. For
micro-industries,
amended technology up gradation funds scheme(at UFS)
should be revived for technology upgrade, as pli2. O will
not cover micro-industries
within its scope' he said.
Thakur stated that due to
the unavailability of quality
man-made fiber(mm) fabric
from indigenous sources, garment exporters are often
dependent on fabric nominated by foreign buyers. He
scheme of special advance
authorization" for fabric
import is" not suitable for garment exporters" due to ever-changing market dynamics,
designs, patterns, shapes, sizes,
geography-specific consumption norms.'''
script = generate_military_script(summary_text)

print(script)