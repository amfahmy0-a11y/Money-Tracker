FINANCIAL_ADVICE = {
    "ar": [
        "🌟 'الاستثمار في المعرفة يحقق دائمًا أفضل العوائد.' — بنجامين فرانكلين.",
        "📊 قاعدة 50/30/20 العالمية: 50% للاحتياجات، 30% للرغبات، 20% للادخار.",
        "💰 'لا تدخر ما يتبقى بعد الإنفاق، بل أنفق ما يتبقى بعد الادخار.' — وارن بافيت.",
        "🛍️ احذر من 'التضخم المعيشي' رفع مستوى المصاريف تلقائيًا مع زيادة الدخل.",
        "📖 ركز على شراء الأصول (تضع المال في جيبك) وتجنب الخصوم (تسحب المال).",
        "🚨 ابنِ 'صندوق الطوارئ' يغطي مصاريف 3 إلى 6 أشهر.",
        "🔄 الحرية المالية = 'الدخل السلبي' (جعل المال يعمل لأجلك).",
        "📈 قاعدة الـ 4%: إذا عشت على 4% من استثماراتك سنويًا، حققت الحرية."
    ],
    "en": [
        "🌟 'An investment in knowledge pays the best interest.' — Benjamin Franklin.",
        "📊 The 50/30/20 Rule: 50% Needs, 30% Wants, 20% Savings.",
        "💰 'Do not save what is left after spending, but spend what is left after saving.' — Warren Buffett.",
        "🛍️ Beware of 'Lifestyle Inflation' as your income rises.",
        "📖 Focus on acquiring assets (put money in pocket) over liabilities.",
        "🚨 Build an 'Emergency Fund' covering 3-6 months of expenses.",
        "🔄 Financial Freedom = 'Passive Income' (money working for you).",
        "📈 The 4% Rule: Live annually on 4% of your portfolio."
    ]
}

def get_advice_by_hour(lang="ar") -> str:
    import datetime
    current_hour = datetime.datetime.now().hour
    advice_list = FINANCIAL_ADVICE.get(lang, FINANCIAL_ADVICE["ar"])
    index = current_hour % len(advice_list)
    return advice_list[index]
