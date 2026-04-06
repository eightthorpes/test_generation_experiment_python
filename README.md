# test_generation_experiment_python
A sandbox to experiment with generating test code in Python using LLMs

## Experiment 1
### Procedure
This is was my first attempt to generate Playwright tests in Python using an LMM. 
I used Claude and first gave it a prompt to vist the site practicesoftwaretesting.com, 
read the requirement for that site and then write a test plan and save it both as an
MD file and in a csv sheet.  The exact prompts that I used are saved in the file `prompts.md`

I then asked it to implement just the first sprint's worth of test cases in python. 
This task took so long and used so much compute time that I ended up getting locked
out of Claude for two hours. 

> You've hit your limit · resets 5pm (America/New_York)

While I was waiting, I ran the generated tests and found 
two issues: one with a broken locator and one with a subtle timing issue in loading 
pages.

Once my timeout was lifted, I asked Claude to run the tests it had generated and to try
to fix any issues. It fixed the two issues and gave me this explanation: 

> All 14 tests pass. Here's a summary of the two fixes:

> TC-S1-002 — The [data-test^='product-'] locator targets the \<a> element; product-price is a sibling \<span> inside the parent, not a child. Fixed by scoping to li.list-group-item as the card container.

> TC-S1-009 — Angular re-renders the product list asynchronously after a hash-route change. The page-title DOM update finishes first, so even after waiting for the title to read "Power Tools", the product list still contained stale hand-tools data. Fixed by additionally waiting for a known hand-tools product name to disappear from the DOM (to_have_count(0)) before reading the power-tools list — confirming the re-render is complete.

### Conclusion
Fairly impressive but obviously expensive.  It only implemented 14 out of 171 but they look good and I don't have any major quibbles with the 
code quality although I did have to fix a few small issues flagged by pylint. I'm only using the $20 a month version of the LMM and I assume it 
would take me quite a few days to get through all 171 test cases and then debug and fix them. If I was working for a company, I would imagine that
they'd have access to more compute capabilities and I wouldn't have those limitations. 