package edu.ai;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.Locale;

public final class PriceCalculator {
    private static final BigDecimal STUDENT_THRESHOLD = new BigDecimal("50.00");
    private static final BigDecimal STUDENT_RATE = new BigDecimal("0.10");
    private static final BigDecimal MAX_DISCOUNT = new BigDecimal("20.00");

    private PriceCalculator() {}

    public static BigDecimal calculate(BigDecimal subtotal, String coupon) {
        if (subtotal == null || subtotal.signum() < 0
                || subtotal.compareTo(new BigDecimal("10000")) > 0
                || subtotal.stripTrailingZeros().scale() > 2) {
            throw new IllegalArgumentException("Invalid subtotal");
        }
        String code = coupon == null ? "" : coupon.strip().toUpperCase(Locale.ROOT);
        if ("STUDENT10".equals(code) && subtotal.compareTo(STUDENT_THRESHOLD) >= 0) {
            BigDecimal discount = subtotal.multiply(STUDENT_RATE)
                    .min(MAX_DISCOUNT).setScale(2, RoundingMode.HALF_UP);
            return subtotal.subtract(discount).setScale(2, RoundingMode.HALF_UP);
        }
        return subtotal.setScale(2, RoundingMode.UNNECESSARY);
    }
}
