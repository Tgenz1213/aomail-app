from aomail.email_providers.imap.utils import get_imap_email_id


def test_get_imap_email_id():
    assert (
        get_imap_email_id(("<Bhit1ZtWVkWqyXNbQwdXcw@notifications.google.com>",))
        == "Bhit1ZtWVkWqyXNbQwdXcw@notifications.google.com"
    )
    assert (
        get_imap_email_id(("<fKV5TKolhqO--dQMhbnSCg@notifications.google.com>",))
        == "fKV5TKolhqO--dQMhbnSCg@notifications.google.com"
    )
    assert (
        get_imap_email_id(
            (
                "\r\n <DU0PR10MB7052CBFED79FC823749C55E2DDD12@DU0PR10MB7052.EURPRD10.PROD.OUTLOOK.COM>",
            )
        )
        == "DU0PR10MB7052CBFED79FC823749C55E2DDD12@DU0PR10MB7052.EURPRD10.PROD.OUTLOOK.COM"
    )
    assert (
        get_imap_email_id(
            ("<AC700000000107DF4B9116B80D4efs_mkt_prod2@don.efs.sante.fr>",)
        )
        == "AC700000000107DF4B9116B80D4efs_mkt_prod2@don.efs.sante.fr"
    )
    assert (
        get_imap_email_id(
            (
                "\r\n <AS8P251MB08879403671AEC41C692F13084D62@AS8P251MB0887.EURP251.PROD.OUTLOOK.COM>",
            )
        )
        == "AS8P251MB08879403671AEC41C692F13084D62@AS8P251MB0887.EURP251.PROD.OUTLOOK.COM"
    )
