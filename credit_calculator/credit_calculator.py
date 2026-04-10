import math
import argparse
import sys


class CreditCalc:
    def __init__(self, args):
        self.calc_type = args.type
        self.total_credit = args.principal
        self.monthly_sum = args.payment
        self.months_count = args.periods
        self.yearly_interest = args.interest

        # Валидация процента
        if self.yearly_interest is None or self.yearly_interest <= 0:
            print("Параметры введены неверно.")
            sys.exit()

        # Месячная ставка (i)
        self.i = self.yearly_interest / (12 * 100)

    def _print_extra(self, total_spent, base_sum):
        print(f"Переплата: {int(total_spent - base_sum)}")

    def calc_annuity_payment(self):
        # Поиск ежемесячного взноса (A)
        pow_val = math.pow(1 + self.i, self.months_count)
        pay = self.total_credit * (self.i * pow_val) / (pow_val - 1)
        pay = math.ceil(pay)
        print(f"Ваш платеж на каждый месяц = {pay}")
        self._print_extra(pay * self.months_count, self.total_credit)

    def calc_principal_sum(self):
        # Поиск основной суммы (P)
        pow_val = math.pow(1 + self.i, self.months_count)
        p_value = self.monthly_sum / ((self.i * pow_val) / (pow_val - 1))
        p_value = math.floor(p_value)
        print(f"Сумма займа составит: {p_value}")
        self._print_extra(self.monthly_sum * self.months_count, p_value)

    def calc_duration(self):
        # Поиск срока (n)
        inner_log = self.monthly_sum / (self.monthly_sum - self.i * self.total_credit)
        n_months = math.ceil(math.log(inner_log, 1 + self.i))

        years, remains = divmod(n_months, 12)
        output_parts = []
        if years > 0:
            y_word = "год" if years == 1 else "года" if 2 <= years <= 4 else "лет"
            output_parts.append(f"{years} {y_word}")
        if remains > 0:
            m_word = "месяц" if remains == 1 else "месяца" if 2 <= remains <= 4 else "месяцев"
            output_parts.append(f"{remains} {m_word}")

        print(f"Для погашения нужно: {' и '.join(output_parts)}")
        self._print_extra(self.monthly_sum * n_months, self.total_credit)

    def calc_diff_payments(self):
        # Дифференцированная схема
        total_payout = 0
        for m in range(1, self.months_count + 1):
            # Формула: Dm = P/n + i*(P - P*(m-1)/n)
            dm = (self.total_credit / self.months_count) + \
                 self.i * (self.total_credit - (self.total_credit * (m - 1) / self.months_count))
            dm = math.ceil(dm)
            total_payout += dm
            print(f"Месяц {m}: выплата {dm}")

        self._print_extra(total_payout, self.total_credit)

    def is_data_correct(self):
        # Проверка на отрицательные значения
        checks = [self.total_credit, self.monthly_sum, self.months_count, self.yearly_interest]
        if any(v is not None and v < 0 for v in checks):
            return False

        # Условие для дифференцированных платежей (нельзя передавать payment)
        if self.calc_type == "diff" and self.monthly_sum is not None:
            return False

        # Должно быть как минимум 4 параметра (включая interest и type)
        params = [self.total_credit, self.monthly_sum, self.months_count]
        if sum(1 for p in params if p is not None) < 2:
            return False

        return True

    def run_calculation(self):
        if not self.is_data_correct():
            print("Неправильные параметры.")
            return

        if self.calc_type == "annuity":
            if self.monthly_sum is None:
                self.calc_annuity_payment()
            elif self.total_credit is None:
                self.calc_principal_sum()
            elif self.months_count is None:
                self.calc_duration()
        elif self.calc_type == "diff":
            self.calc_diff_payments()
        else:
            print("Тип платежа указан неверно.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Инструмент для расчета кредита")

    parser.add_argument("--type", choices=["annuity", "diff"])
    parser.add_argument("--principal", type=float)
    parser.add_argument("--payment", type=float)
    parser.add_argument("--periods", type=int)
    parser.add_argument("--interest", type=float)

    input_data = parser.parse_args()
    app = CreditCalc(input_data)
    app.run_calculation()