import re
import json


class ReviewSummary:
    def __init__(self, recent=None, overall=None):
        self._recent = recent
        self._overall = overall

    @property
    def recent(self):
        return self._recent

    @property
    def overall(self):
        return self._overall

    def __str__(self):
        return json.dumps(
                {
                    'recent': str(self.recent),
                    'overall': str(self.overall)
                })


class ReviewInfo:
    def __init__(self, opinion, total_rev, like_percent):
        self._opinion = opinion
        self._total_rev = total_rev
        self._like_percent = like_percent

    @property
    def opinion(self):
        return self._opinion

    @property
    def total_review(self):
        return self._total_rev

    @property
    def like_percent(self):
        return self._like_percent

    def __str__(self):
        return json.dumps(
                {
                    'opinion': self.opinion,
                    'total': self.total_review,
                    'like': self.like_percent
                })


def extract(soup):
    review_infos = soup.find_all('div', 'user_reviews_summary_row')
    recent_info = _extract_info(review_infos[0])
    overall_info = None
    if (len(review_infos) > 1):
        overall_info = _extract_info(review_infos[1])

    return ReviewSummary(recent_info, overall_info)


def _extract_info(review_summary_row):
    like_percent, total_review = _extract_data(review_summary_row)
    opinion = review_summary_row.find('span', 'game_review_summary').string
    return ReviewInfo(opinion, total_review, like_percent)


def _extract_data(review_summary_row):
    tooltip = review_summary_row['data-store-tooltip']
    regex = re.compile(r'^(\d+)% of the ([\d,]+?) ')
    match_result = re.match(regex, tooltip).groups()
    return int(match_result[0]) / 100, \
        int(match_result[1].replace(',', ''))


if __name__ == '__main__':
    from bs4 import BeautifulSoup
    from os.path import join
    import os

    sample_dir = '../samples/'
    samples = os.listdir(sample_dir)
    for sample in samples:
        sample_path = join(sample_dir, sample)
        soup = BeautifulSoup(open(sample_path), 'lxml')
        print(extract(soup))