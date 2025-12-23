import json

from ibermatcher.cli_utils import build_emails, load_papers, load_reviewers
from ibermatcher.constraints import get_constraints
from ibermatcher.matchers import match_by_branch_and_bound

# Load your papers and reviewer pools
papers_collection = load_papers("etc/data/papers.xlsx")
reviewers_collection = load_reviewers("etc/data/reviewers.xlsx")


# Define the feasibility constraints
reviewers_per_paper = 2
constraints = get_constraints(
    [
        "reviewer_underload",
        "reviewer_not_author",
        "unique_reviewers",
        "reviewers_from_different_institutions",
        "reviewers_not_authors_institutions",
    ],
    papers_collection,
    reviewers_collection,
    reviewers_per_paper,
)

solution, score = match_by_branch_and_bound(
    papers_collection,
    reviewers_collection,
    constraints,
    reviewers_per_paper,
)

# Create emails
email_template = "Dear {reviewer}, you have been assigned to review the paper titled '{paper}'."
emails = build_emails(
    solution,
    reviewers_collection,
    "Dear {reviewer}, you have been assigned to review the paper titled '{paper}'.",
)

with open("emails.jsonl", "w") as fw:
    for email in emails:
        fw.write(json.dumps({"to": email.to, "content": email.content}) + "\n")
