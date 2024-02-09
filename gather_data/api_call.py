def call_api():

    from google.oauth2 import service_account

    from google.analytics.data_v1beta import BetaAnalyticsDataClient

    from google.analytics.data_v1beta.types import (
        DateRange,
        Dimension,
        Metric,
        RunReportRequest,
    )

    property_id = '<INSERT_GOOGLE_ANALYTICS_ASSET_PROPRTY_ID>'

    keys = '<INSERT_JSON_KEY_FOR_SERVICE_ACCOUNT_CREDENTIALS_VERIFICATION>'

    credentials = service_account.Credentials.from_service_account_file(filename=keys)

    client = BetaAnalyticsDataClient(credentials=credentials)

    dim_list = [Dimension(name='date'),
                Dimension(name='sessionDefaultChannelGroup'),
                Dimension(name='landingPagePlusQueryString')
                ]

    met_list = [Metric(name="totalUsers"),
                Metric(name="conversions")
                ]

    def run_report(property_id):
        request = RunReportRequest(

            property=f"properties/{property_id}",

            dimensions=dim_list,

            metrics=met_list,

            date_ranges=[
                DateRange(start_date="2020-03-31",
                          end_date="today")
            ],

        )
        return client.run_report(request)

    response = run_report(property_id)

    return(response)
